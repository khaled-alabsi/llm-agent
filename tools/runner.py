"""Shell runner tool definitions used by the coder agent.

Runs non-interactive bash commands inside the active workspace directory and
returns exit code, stdout, and stderr.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Optional, Tuple

from helpers.file_utils import Workspace

ToolSpec = Tuple[str, Callable[..., Any], Dict[str, Any]]


class RunnerTools:
    """Expose a simple shell runner to the LLM."""

    def __init__(self, workspace_supplier: Callable[[], Workspace]):
        self._workspace_supplier = workspace_supplier

    def tool_specs(self) -> Iterable[ToolSpec]:
        yield ("run_shell", self.run_shell, RUN_SHELL_SCHEMA)

    def _workspace_root(self, cwd: Optional[str] = None) -> Path:
        workspace = self._workspace_supplier()
        root = workspace.root
        if cwd:
            candidate = (root / cwd).resolve()
            if root not in candidate.parents and candidate != root:
                raise ValueError("cwd must be inside the active workspace")
            return candidate
        return root

    def run_shell(self, command: str, timeout_sec: int = 20, cwd: Optional[str] = None) -> Dict[str, Any]:
        if not command or not isinstance(command, str):
            return {"status": "error", "message": "command must be a non-empty string"}

        workdir = self._workspace_root(cwd)

        try:
            proc = subprocess.run(
                ["/usr/bin/env", "bash", "-lc", command],
                cwd=str(workdir),
                capture_output=True,
                text=True,
                timeout=timeout_sec,
            )
            return {
                "status": "success" if proc.returncode == 0 else "error",
                "exit_code": proc.returncode,
                "stdout": proc.stdout[-10000:],
                "stderr": proc.stderr[-10000:],
                "cwd": str(workdir),
                "command": command,
            }
        except subprocess.TimeoutExpired as exc:
            return {
                "status": "error",
                "message": f"timeout after {timeout_sec}s",
                "stdout": exc.stdout or "",
                "stderr": exc.stderr or "",
                "cwd": str(workdir),
                "command": command,
            }


RUN_SHELL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "run_shell",
        "description": "Run a non-interactive bash command inside the active workspace root and return exit code, stdout, and stderr.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The bash command to execute."},
                "timeout_sec": {
                    "type": "integer",
                    "description": "Timeout in seconds (default 20).",
                    "default": 20,
                },
                "cwd": {
                    "type": "string",
                    "description": "Optional working directory relative to workspace root.",
                },
            },
            "required": ["command"],
        },
    },
}

