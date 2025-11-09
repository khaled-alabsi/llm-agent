"""Agent implementations for building Python projects."""

from __future__ import annotations

import json
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import requests

from core.config import LLMConfig
from core.context_loader import load_context, load_skills
from helpers import Workspace, get_logger, slugify
from tools.filesystem import FilesystemTools
from tools.runner import RunnerTools


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

    def register_tool(self, name: str, func: Callable[..., Any], schema: Dict[str, Any]) -> None:
        self.tools[name] = func
        self.tool_schemas.append(schema)

    def reset_conversation(self) -> None:
        self.conversation_history = []
        self.request_count = 0

    def _save_json(self, payload: Dict[str, Any], prefix: str) -> None:
        if not self._log_dir_path:
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = self._log_dir_path / f"{prefix}_{self.request_count}_{timestamp}.json"
        file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

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
        self._save_json(payload, "request")

        if self.verbose:
            self.logger.info("Sending payload to LLM: %s", json.dumps(payload, indent=2))

        response = requests.post(
            f"{self.base_url}/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=120,
        )
        response.raise_for_status()
        result = response.json()

        self._save_json(result, "response")
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

        for _ in range(max_iterations):
            response = self.call_llm(self.conversation_history)
            text_content, tool_calls = self.parse_response(response)
            final_text = text_content or final_text

            assistant_message: Dict[str, Any] = {"role": "assistant", "content": text_content}
            if tool_calls:
                assistant_message["tool_calls"] = tool_calls
            self.conversation_history.append(assistant_message)

            if not tool_calls:
                return final_text

            for tool_call in tool_calls:
                tool_name = tool_call.get("function", {}).get("name")
                arguments = tool_call.get("function", {}).get("arguments")
                tool_id = tool_call.get("id") or tool_name or "tool"
                result = self.execute_tool(tool_name, arguments)
                tool_response = result
                if isinstance(result, (dict, list)):
                    tool_response = json.dumps(result)
                self.conversation_history.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "name": tool_name,
                        "content": tool_response if isinstance(tool_response, str) else str(tool_response),
                    }
                )

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

    
