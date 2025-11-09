"""Filesystem tool definitions used by the coder agent."""

from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, Optional, Tuple

from helpers.file_utils import Workspace

ToolSpec = Tuple[str, Callable[..., Any], Dict[str, Any]]


class FilesystemTools:
    """Bundle of filesystem operations exposed to the LLM."""

    def __init__(self, workspace_supplier: Callable[[], Workspace]):
        self._workspace_supplier = workspace_supplier

    def tool_specs(self) -> Iterable[ToolSpec]:
        yield ("write_file", self.write_file, WRITE_FILE_SCHEMA)
        yield ("read_file", self.read_file, READ_FILE_SCHEMA)
        yield ("list_files", self.list_files, LIST_FILES_SCHEMA)
        yield ("describe_workspace", self.describe_workspace, DESCRIBE_WORKSPACE_SCHEMA)

    def _workspace(self) -> Workspace:
        workspace = self._workspace_supplier()
        if workspace is None:
            raise RuntimeError("No active workspace. Call build_project() first.")
        return workspace

    def write_file(self, path: str, content: str, overwrite: bool = True) -> Dict[str, Any]:
        return self._workspace().write_file(path, content, overwrite=overwrite)

    def read_file(self, path: str) -> Dict[str, Any]:
        return self._workspace().read_file(path)

    def list_files(self, pattern: Optional[str] = None, max_results: int = 200) -> Dict[str, Any]:
        return self._workspace().list_files(pattern=pattern, max_results=max_results)

    def describe_workspace(self, max_lines: int = 200) -> Dict[str, Any]:
        return self._workspace().describe(max_lines=max_lines)


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
                    "description": "Overwrite existing file when true",
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
            "properties": {"path": {"type": "string", "description": "Relative file path"}},
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
                    "description": "Optional glob such as 'src/*.py'",
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

FILESYSTEM_SCHEMAS = (
    WRITE_FILE_SCHEMA,
    READ_FILE_SCHEMA,
    LIST_FILES_SCHEMA,
    DESCRIBE_WORKSPACE_SCHEMA,
)
