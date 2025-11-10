"""Agent implementations for building Python projects."""

from __future__ import annotations

import json
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import requests

from core.config import LLMConfig
from core.llm import LLMClient
from core.context_loader import load_context, load_skills
from helpers import Workspace, get_logger, slugify
from tools.filesystem import FilesystemTools
from tools.runner import RunnerTools
from tools.history import HistoryTools
from helpers.file_utils import slugify


class ToolCallingAgent:
    """Minimal agent wrapper for local LLMs with tool-calling enabled."""

    def __init__(self, config: Optional[LLMConfig] = None, *, verbose: bool = False):
        self.config = config or LLMConfig.load()
        self.base_url = self.config.base_url.rstrip("/")
        self.verbose = verbose
        self.logger = get_logger(__name__, self.config.log_dir)

        self.tools: Dict[str, Callable[..., Any]] = {}
        self.tool_schemas: List[Dict[str, Any]] = []
        self.request_count = 0
        self.conversation_history: List[Dict[str, Any]] = []

        self._log_dir_path = self.config.prepare_log_dir()
        self._log_file_path: Optional[Path] = (
            (self._log_dir_path / "agent.log.json") if self._log_dir_path else None
        )
        self._sessions_root: Optional[Path] = (
            (self._log_dir_path / "sessions") if self._log_dir_path else None
        )
        self._session_dir: Optional[Path] = None
        self._session_log_path: Optional[Path] = None
        self._tools_dir: Optional[Path] = None
        self._session_index: int = 0
        self.llm = LLMClient(self.config)
        self._history_tools = HistoryTools(lambda: self.llm)
        self._tool_seq: int = 0

    def register_tool(self, name: str, func: Callable[..., Any], schema: Dict[str, Any]) -> None:
        self.tools[name] = func
        self.tool_schemas.append(schema)

    def reset_conversation(self) -> None:
        self.conversation_history = []
        self.request_count = 0
        self._begin_session()
        self._tool_seq = 0

    def _begin_session(self) -> None:
        if not self._log_file_path:
            return
        self._session_index += 1
        # Prepare per-session directory structure
        try:
            if self._sessions_root:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                self._sessions_root.mkdir(parents=True, exist_ok=True)
                self._session_dir = self._sessions_root / f"session_{self._session_index}_{ts}"
                self._session_dir.mkdir(parents=True, exist_ok=True)
                self._tools_dir = self._session_dir / "tools"
                self._tools_dir.mkdir(parents=True, exist_ok=True)
                self._session_log_path = self._session_dir / "session.log.json"
                meta = {
                    "session_index": self._session_index,
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                }
                (self._session_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            self.logger.warning("Failed to init session dir: %s", exc)

        header = {
            "type": "session_start",
            "session_index": self._session_index,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
        self._append_session_entry(header)

    def _append_session_entry(self, entry: Dict[str, Any]) -> None:
        if not self._log_file_path:
            return
        try:
            # Load existing pretty JSON array (single-file log)
            if self._log_file_path.exists():
                try:
                    existing = json.loads(self._log_file_path.read_text(encoding="utf-8"))
                    if not isinstance(existing, list):
                        existing = []
                except Exception:
                    existing = []
            else:
                existing = []
            existing.append(entry)
            self._write_log_file(existing)
        except Exception as exc:  # noqa: BLE001
            # Fall back to console logging if file write fails
            self.logger.warning("Failed to append session log: %s", exc)
        # Also write to per-session log file
        try:
            if self._session_log_path:
                if self._session_log_path.exists():
                    try:
                        sess_existing = json.loads(self._session_log_path.read_text(encoding="utf-8"))
                        if not isinstance(sess_existing, list):
                            sess_existing = []
                    except Exception:
                        sess_existing = []
                else:
                    sess_existing = []
                sess_existing.append(entry)
                self._write_log_file(sess_existing, path=self._session_log_path)
        except Exception as exc:  # noqa: BLE001
            self.logger.warning("Failed to append per-session log: %s", exc)

    def _write_log_file(self, entries: List[Dict[str, Any]], *, path: Optional[Path] = None) -> None:
        """Write the log as a pretty JSON array with visual separation.

        Adds five blank lines between entries for readability while keeping
        the file valid JSON.
        """
        log_path = path or self._log_file_path
        if not log_path:
            return
        try:
            sep = "\n\n\n\n\n"  # five empty lines
            with log_path.open("w", encoding="utf-8") as f:
                f.write("[\n")
                for i, e in enumerate(entries):
                    block = json.dumps(e, indent=2, ensure_ascii=False)
                    indented = "\n".join("  " + line for line in block.splitlines())
                    f.write(indented)
                    if i != len(entries) - 1:
                        f.write("," + sep)
                    else:
                        f.write("\n")
                f.write("]\n")
        except Exception as exc:  # noqa: BLE001
            self.logger.warning("Failed to write log file: %s", exc)

    def _write_tool_io(self, *, name: str, stage: str, payload: Dict[str, Any]) -> None:
        """Write a tool input/output JSON next to the session log."""
        if not self._tools_dir:
            return
        try:
            self._tool_seq += 1
            safe = slugify(name) or "tool"
            file_path = self._tools_dir / f"tool_{self._tool_seq:03d}_{safe}_{stage}.json"
            file_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            self.logger.warning("Failed to write tool IO: %s", exc)

    # Pretty session files were removed to enforce a single log file policy.

    def call_llm(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }
        if self.tool_schemas:
            payload["tools"] = self.tool_schemas
            payload["tool_choice"] = "auto"

        self.request_count += 1
        self._append_session_entry({
            "type": "request",
            "request_index": self.request_count,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "payload": payload,
        })

        if self.verbose:
            self.logger.info("Sending payload to LLM: %s", json.dumps(payload, indent=2))

        # Delegate actual HTTP call to the LLM client abstraction
        result = self.llm.chat(
            messages,
            tools=self.tool_schemas if self.tool_schemas else None,
            tool_choice="auto",
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )

        self._append_session_entry({
            "type": "response",
            "request_index": self.request_count,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "payload": result,
        })
        if self.verbose:
            self.logger.info("Received response from LLM: %s", json.dumps(result, indent=2))

        return result

    @staticmethod
    def parse_response(response: Dict[str, Any]) -> tuple[str, List[Dict[str, Any]]]:
        choice = response.get("choices", [{}])[0]
        message = choice.get("message", {})
        text_content = message.get("content") or ""
        tool_calls = message.get("tool_calls") or []
        return text_content, tool_calls

    @staticmethod
    def _finish_reason(response: Dict[str, Any]) -> str | None:
        choice = response.get("choices", [{}])[0]
        return choice.get("finish_reason")

    def execute_tool(self, tool_name: str, arguments: Any) -> Any:
        tool = self.tools.get(tool_name)
        if not tool:
            return {"status": "error", "message": f"Unknown tool '{tool_name}'", "error_type": "LookupError"}

        if isinstance(arguments, str):
            try:
                args = json.loads(arguments) if arguments else {}
            except Exception as exc:  # noqa: BLE001
                return {
                    "status": "error",
                    "message": f"Invalid JSON arguments: {exc}",
                    "error_type": exc.__class__.__name__,
                }
        else:
            args = arguments or {}

        try:
            return tool(**args)
        except Exception as exc:  # noqa: BLE001
            return {
                "status": "error",
                "message": str(exc),
                "error_type": exc.__class__.__name__,
            }

    def run(self, messages: List[Dict[str, Any]], max_iterations: int = 8) -> str:
        self.conversation_history = [dict(message) for message in messages]
        final_text = ""
        # Mark run start in the log
        try:
            user_msgs = [m.get("content", "") for m in messages if m.get("role") == "user"]
            self._append_session_entry({
                "type": "run_start",
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "max_iterations": max_iterations,
                "user_message": user_msgs[-1] if user_msgs else "",
            })
        except Exception:
            pass

        for _ in range(max_iterations):
            response = self.call_llm(self.conversation_history)
            finish_reason = self._finish_reason(response)
            text_content, tool_calls = self.parse_response(response)
            final_text = text_content or final_text

            assistant_message: Dict[str, Any] = {"role": "assistant", "content": text_content}
            if tool_calls:
                assistant_message["tool_calls"] = tool_calls
            # If the model stopped due to length and gave no tool calls, compact history and retry
            if (finish_reason == "length") and (not tool_calls):
                # Log history tool input
                self._write_tool_io(
                    name="summarize_history",
                    stage="input",
                    payload={
                        "keep_last_n": 6,
                        "messages": self.conversation_history,
                    },
                )
                compact = self._history_tools.summarize_history(self.conversation_history, keep_last_n=6)
                # Log history tool output
                self._write_tool_io(
                    name="summarize_history",
                    stage="output",
                    payload=compact if isinstance(compact, dict) else {"status": "error", "messages": []},
                )
                before = len(self.conversation_history)
                after = len(compact.get("messages", [])) if isinstance(compact, dict) else before
                self._append_session_entry({
                    "type": "history_compacted",
                    "before": before,
                    "after": after,
                    "status": compact.get("status"),
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                })
                msgs = compact.get("messages") if isinstance(compact, dict) else None
                if msgs:
                    self.conversation_history = msgs
                    # Do not append the truncated assistant message; retry loop
                    continue
                # If we couldn't compact, fall through to append as-is
            self.conversation_history.append(assistant_message)

            if not tool_calls:
                # No more tool calls; agent is done
                self._append_session_entry({
                    "type": "run_end",
                    "reason": "no_tool_calls",
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "final_text": final_text,
                })
                return final_text

            for tool_call in tool_calls:
                tool_name = tool_call.get("function", {}).get("name")
                arguments = tool_call.get("function", {}).get("arguments")
                tool_id = tool_call.get("id") or tool_name or "tool"
                # Log tool call + write input file
                parsed_args = arguments
                if isinstance(arguments, str):
                    try:
                        parsed_args = json.loads(arguments) if arguments else {}
                    except Exception:
                        parsed_args = {"_raw": arguments}
                self._append_session_entry({
                    "type": "tool_call",
                    "tool_call_id": tool_id,
                    "name": tool_name,
                    "args": parsed_args,
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                })
                self._write_tool_io(
                    name=tool_name or "unknown",
                    stage="input",
                    payload={"tool_call_id": tool_id, "args": parsed_args},
                )

                result = self.execute_tool(tool_name, arguments)
                # Normalize tool result so the LLM can reliably react to errors
                normalized = {
                    "tool": tool_name,
                    "args": parsed_args,
                    "status": None,
                    "ok": False,
                    "data": None,
                    "error": None,
                }
                if isinstance(result, dict):
                    status = result.get("status")
                    normalized["status"] = status
                    normalized["ok"] = (status == "success")
                    if normalized["ok"]:
                        normalized["data"] = {k: v for k, v in result.items() if k != "status"}
                    else:
                        normalized["error"] = {
                            "type": result.get("error_type") or "ToolError",
                            "message": result.get("message") or "",
                        }
                        extra = {k: v for k, v in result.items() if k not in {"status", "message", "error_type"}}
                        if extra:
                            normalized["error"]["extra"] = extra
                else:
                    normalized["status"] = "success"
                    normalized["ok"] = True
                    normalized["data"] = result

                tool_response = json.dumps(normalized, ensure_ascii=False)
                self.conversation_history.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "name": tool_name,
                        "content": tool_response,
                    }
                )
                # Write tool output file
                self._write_tool_io(
                    name=tool_name or "unknown",
                    stage="output",
                    payload={"tool_call_id": tool_id, "result": result},
                )
                # Log tool result
                self._append_session_entry({
                    "type": "tool_result",
                    "tool_call_id": tool_id,
                    "name": tool_name,
                    "result": result,
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                })

        # Hit iteration cap
        self._append_session_entry({
            "type": "run_end",
            "reason": "max_iterations",
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "final_text": final_text,
        })
        return final_text or "Max iterations reached without a final answer."


class CoderAgent(ToolCallingAgent):
    """High-level helper that assembles Python projects inside isolated workspaces."""

    def __init__(
        self,
        *,
        config: Optional[LLMConfig] = None,
        project_root: str | Path = "generated_projects",
        context_dir: str | Path = "context",
        verbose: bool = False,
    ):
        super().__init__(config=config, verbose=verbose)
        self.project_root = Path(project_root).expanduser().resolve()
        self.project_root.mkdir(parents=True, exist_ok=True)
        self.context_dir = Path(context_dir)
        self.active_workspace: Optional[Workspace] = None
        # Base skill always included so the agent has general build guidance
        self.base_skills: list[str] = ["coder"]

        self._filesystem_tools = FilesystemTools(self._require_workspace)
        for name, func, schema in self._filesystem_tools.tool_specs():
            self.register_tool(name, func, schema)

        # Register shell runner tools
        self._runner_tools = RunnerTools(self._require_workspace)
        for name, func, schema in self._runner_tools.tool_specs():
            self.register_tool(name, func, schema)

    def _require_workspace(self) -> Workspace:
        if not self.active_workspace:
            raise RuntimeError("No active workspace. Call build_project() first.")
        return self.active_workspace

    def build_project(
        self,
        project_description: str,
        project_name: Optional[str] = None,
        max_iterations: int = 8,
        skills: Optional[list[str]] = None,
    ) -> str:
        slug = slugify(project_name or project_description)
        project_path = self.project_root / slug
        self.active_workspace = Workspace(project_path)
        self.reset_conversation()

        # Merge base skills with caller-provided skills (preserve order, no dups)
        merged_skills: list[str] = []
        for s in (self.base_skills + (skills or [])):
            if s not in merged_skills:
                merged_skills.append(s)

        system_message = self._system_prompt(project_path, skills=merged_skills)
        initial_messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": project_description.strip()},
        ]
        return self.run(initial_messages, max_iterations=max_iterations)

    def _system_prompt(self, project_path: Path, *, skills: list[str]) -> str:
        context_blob = load_context(self.context_dir)
        skills_root = self.context_dir / "skills"
        skills_blob = load_skills(skills_root, skills) if skills else ""
        combined_context = "\n\n".join([x for x in [context_blob, skills_blob] if x]).strip() or "No extra context provided."
        base_instruction = textwrap.dedent(
            f"""
            You are a focused software engineer.
            Build a small but complete project inside '{project_path}'.

            - Follow the brief precisely and avoid hidden fallbacks.
            - Use the available tools to plan, create files, and run shell commands when needed.
            - Prefer minimal dependencies and a clear, runnable structure.
            - Provide a concise summary at the end with run instructions.

            Reference material and skills:
            {combined_context}
            """
        ).strip()

        print("Using base_instruction:", base_instruction)
        return base_instruction

    
