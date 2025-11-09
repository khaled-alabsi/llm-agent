"""Filesystem helpers used by the coder agent."""

from __future__ import annotations

import re
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Dict, List, Optional


class Workspace:
    """Scoped utility for interacting with files inside a project directory."""

    def __init__(self, root: Path | str):
        self.root = Path(root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _resolve(self, incoming_path: str) -> Path:
        """Resolve a user-provided path to an absolute path inside the workspace.

        Accepts either relative paths (recommended) or absolute paths that are
        already inside the workspace. Rejects any path pointing outside.
        """
        if not incoming_path or not str(incoming_path).strip():
            raise ValueError("Path must point to a file inside the workspace")

        p = Path(incoming_path).expanduser()

        if p.is_absolute():
            candidate = p.resolve()
            if self.root not in candidate.parents and candidate != self.root:
                raise ValueError("Access outside the workspace root is not allowed")
            return candidate

        # Relative path: anchor to workspace root first, then resolve
        candidate = (self.root / p).resolve()
        if self.root not in candidate.parents and candidate != self.root:
            raise ValueError("Access outside the workspace root is not allowed")
        return candidate

    def write_file(self, path: str, content: str, overwrite: bool = True) -> Dict[str, Any]:
        file_path = self._resolve(path)
        if not isinstance(content, str):
            raise TypeError(
                f"write_file.content must be a string, got {type(content).__name__}"
            )
        if file_path.exists() and not overwrite:
            raise FileExistsError(f"File '{path}' already exists")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return {
            "status": "success",
            "action": "write_file",
            "path": str(file_path.relative_to(self.root)),
            "size": len(content),
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
            "content": content,
        }

    def list_files(self, pattern: Optional[str] = None, max_results: int = 200) -> Dict[str, Any]:
        paths: List[Dict[str, Any]] = []
        for file_path in sorted(self.root.rglob("*")):
            if not file_path.is_file():
                continue
            rel_path = file_path.relative_to(self.root).as_posix()
            if pattern and not fnmatch(rel_path, pattern):
                continue
            paths.append({"path": rel_path, "size": file_path.stat().st_size})
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
        return {"status": "success", "action": "describe_workspace", "summary": "\n".join(lines)}


def slugify(value: str) -> str:
    """Convert free-form text to a filesystem-friendly slug."""

    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "python-project"
