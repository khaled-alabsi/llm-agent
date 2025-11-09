"""Simple coder agent that builds Python projects via tool-calling."""

from __future__ import annotations

import json
import re
import textwrap
from datetime import datetime
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import requests


class Workspace:
    """Utility class for scoped file operations inside a project directory."""

    def __init__(self, root: Path | str):
        self.root = Path(root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _resolve(self, relative_path: str) -> Path:
        relative_path = relative_path.strip().lstrip("./")
        if not relative_path:
            raise ValueError("Path must point to a file inside the workspace")
        candidate = (self.root / relative_path).resolve()
        if self.root not in candidate.parents and candidate != self.root:
            raise ValueError("Access outside the workspace root is not allowed")
        return candidate

    def write_file(self, path: str, content: str, overwrite: bool = True) -> Dict[str, Any]:
        file_path = self._resolve(path)
        if file_path.exists() and not overwrite:
            raise FileExistsError(f"File '{path}' already exists")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return {
            "status": "success",
            "action": "write_file",
            "path": str(file_path.relative_to(self.root)),
            "size": len(content)
        }

    def read_file(self, path: str) -> Dict[str, Any]:
        file_path = self._resolve(path)
        if not file_path.exists():
            raise FileNotFoundError(f"File '{path}' does not exist")
        content = file_path.read_text(encoding="utf-8")
        return {
            "status": "success",
            "action": "read_file",
            "path": str(file_path.relative_to(self.root)),
            "size": len(content),
            "content": content
        }

    def list_files(self, pattern: Optional[str] = None, max_results: int = 200) -> Dict[str, Any]:
        paths: List[Dict[str, Any]] = []
        for file_path in sorted(self.root.rglob("*")):
            if not file_path.is_file():
                continue
            rel_path = file_path.relative_to(self.root).as_posix()
            if pattern and not fnmatch(rel_path, pattern):
                continue
            paths.append({
                "path": rel_path,
                "size": file_path.stat().st_size
            })
            if len(paths) >= max_results:
                break
        return {"status": "success", "action": "list_files", "files": paths}

    def describe(self, max_lines: int = 200) -> Dict[str, Any]:
        lines: List[str] = []
        for node in sorted(self.root.rglob("*")):
            rel = node.relative_to(self.root).as_posix()
            depth = rel.count("/")
            marker = "dir " if node.is_dir() else "file"
            lines.append(f"{'  ' * depth}{marker}: {rel}")
            if len(lines) >= max_lines:
                break
        if not lines:
            lines = ["(workspace is currently empty)"]
        return {
            "status": "success",
            "action": "describe_workspace",
            "summary": "\n".join(lines)
        }


class ToolCallingAgent:
    """Minimal agent wrapper to talk to a local LLM with tool-calling enabled."""

    def __init__(
        self,
        base_url: str = "http://localhost:1234/v1",
        model: str = "qwen/qwen3-coder-30b",
        log_dir: Optional[str] = "logs",
        temperature: float = 0.2,
        max_tokens: int = 2000,
        verbose: bool = False,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.verbose = verbose

        self.tools: Dict[str, Callable[..., Any]] = {}
        self.tool_schemas: List[Dict[str, Any]] = []
        self.request_count = 0
        self.conversation_history: List[Dict[str, Any]] = []

        self.log_dir = Path(log_dir) if log_dir else None
        if self.log_dir:
            self.log_dir.mkdir(parents=True, exist_ok=True)

    def register_tool(self, name: str, func: Callable[..., Any], schema: Dict[str, Any]) -> None:
        self.tools[name] = func
        self.tool_schemas.append(schema)

    def _save_json(self, payload: Dict[str, Any], prefix: str) -> None:
        if not self.log_dir:
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = self.log_dir / f"{prefix}_{self.request_count}_{timestamp}.json"
        file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def call_llm(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if self.tool_schemas:
            payload["tools"] = self.tool_schemas
            payload["tool_choice"] = "auto"

        self.request_count += 1
        self._save_json(payload, "request")

        if self.verbose:
            print("Sending payload to LLM:")
            print(json.dumps(payload, indent=2))

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=120,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(f"LLM request failed: {exc}") from exc

        result = response.json()
        self._save_json(result, "response")

        if self.verbose:
            print("Received response from LLM:")
            print(json.dumps(result, indent=2))

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
            return {"error": f"Unknown tool '{tool_name}'"}

        if isinstance(arguments, str):
            try:
                args = json.loads(arguments) if arguments else {}
            except json.JSONDecodeError as exc:
                return {"error": f"Invalid arguments for {tool_name}: {exc}"}
        else:
            args = arguments or {}

        try:
            return tool(**args)
        except TypeError as exc:
            return {"error": f"Invalid parameters for {tool_name}: {exc}"}
        except Exception as exc:  # noqa: BLE001
            return {"error": f"Tool '{tool_name}' raised an error: {exc}"}

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

    def reset_conversation(self) -> None:
        self.conversation_history = []


class CoderAgent(ToolCallingAgent):
    """High-level helper that focuses on generating Python projects."""

    def __init__(
        self,
        base_url: str = "http://localhost:1234/v1",
        model: str = "qwen/qwen3-coder-30b",
        log_dir: Optional[str] = "logs",
        project_root: str = "generated_projects",
        verbose: bool = False,
    ):
        super().__init__(base_url=base_url, model=model, log_dir=log_dir, verbose=verbose)
        self.project_root = Path(project_root).expanduser().resolve()
        self.project_root.mkdir(parents=True, exist_ok=True)
        self.active_workspace: Optional[Workspace] = None
        self._register_workspace_tools()

    def _register_workspace_tools(self) -> None:
        self.register_tool("write_file", self._write_file_tool, WRITE_FILE_SCHEMA)
        self.register_tool("read_file", self._read_file_tool, READ_FILE_SCHEMA)
        self.register_tool("list_files", self._list_files_tool, LIST_FILES_SCHEMA)
        self.register_tool("describe_workspace", self._describe_workspace_tool, DESCRIBE_WORKSPACE_SCHEMA)

    def _require_workspace(self) -> Workspace:
        if not self.active_workspace:
            raise RuntimeError("No active workspace. Call build_project() first.")
        return self.active_workspace

    def _write_file_tool(self, path: str, content: str, overwrite: bool = True) -> Dict[str, Any]:
        workspace = self._require_workspace()
        return workspace.write_file(path, content, overwrite=overwrite)

    def _read_file_tool(self, path: str) -> Dict[str, Any]:
        workspace = self._require_workspace()
        return workspace.read_file(path)

    def _list_files_tool(self, pattern: Optional[str] = None, max_results: int = 200) -> Dict[str, Any]:
        workspace = self._require_workspace()
        return workspace.list_files(pattern=pattern, max_results=max_results)

    def _describe_workspace_tool(self, max_lines: int = 200) -> Dict[str, Any]:
        workspace = self._require_workspace()
        return workspace.describe(max_lines=max_lines)

    def build_project(
        self,
        project_description: str,
        project_name: Optional[str] = None,
        max_iterations: int = 8,
    ) -> str:
        slug = slugify(project_name or project_description)
        project_path = self.project_root / slug
        self.active_workspace = Workspace(project_path)
        self.reset_conversation()

        system_message = self._system_prompt(project_path)
        initial_messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": project_description.strip()},
        ]
        return self.run(initial_messages, max_iterations=max_iterations)

    @staticmethod
    def _system_prompt(project_path: Path) -> str:
        return textwrap.dedent(
            f"""
            You are a focused Python engineer. Build a small but complete Python project inside
            '{project_path}'.

            Expectations:
            - Work in clear stages: understand the ask, plan the file layout, implement, then finalise.
            - Use the provided tools to inspect or modify files. Paths must be relative to the project root.
            - Prefer standard library modules. Introduce dependencies only when absolutely necessary.
            - Every project must include a README with usage instructions and, when possible, runnable entry points.
            - Keep responses concise. When the project is ready, end with a short summary and how to run it.
            """.strip()
        )


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "python-project"


WRITE_FILE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Create or overwrite a file inside the active project workspace",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Relative path of the file"},
                "content": {"type": "string", "description": "Complete file contents"},
                "overwrite": {
                    "type": "boolean",
                    "description": "Overwrite existing file if set to true",
                    "default": True,
                },
            },
            "required": ["path", "content"],
        },
    },
}

READ_FILE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Read the contents of a file inside the active project workspace",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Relative file path"}
            },
            "required": ["path"],
        },
    },
}

LIST_FILES_SCHEMA = {
    "type": "function",
    "function": {
        "name": "list_files",
        "description": "List files available inside the active project workspace",
        "parameters": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Optional glob pattern such as 'src/*.py'",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of files to return",
                    "default": 200,
                },
            },
        },
    },
}

DESCRIBE_WORKSPACE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "describe_workspace",
        "description": "Get a condensed summary of the current project tree",
        "parameters": {
            "type": "object",
            "properties": {
                "max_lines": {
                    "type": "integer",
                    "description": "Cap the number of lines in the summary",
                    "default": 200,
                }
            },
        },
    },
}


if __name__ == "__main__":
    coder = CoderAgent()
    example_brief = (
        "Create a minimal task-tracking CLI. It should save tasks to a JSON file and "
        "support adding, listing, and completing tasks. Provide a README with usage."
    )
    print(coder.build_project(example_brief, project_name="task_cli", max_iterations=6))
