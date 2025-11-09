"""
File operation tools for CrewAI agent
"""

from pathlib import Path
from typing import Optional
from crewai.tools import tool


BASE_OUTPUT_DIR = Path("./output").resolve()
BASE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _resolve_output_path(path_str: Optional[str] = None) -> Path:
    """
    Resolve user-provided paths so everything stays inside ./output.

    Strips leading "./", "/", or redundant "output/" segments to avoid nesting like
    "./output/output/...".
    """
    if not path_str or path_str.strip() in {"", ".", "./"}:
        relative = Path(".")
    else:
        cleaned = path_str.strip().replace("\\", "/")
        while cleaned.startswith("./"):
            cleaned = cleaned[2:]
        cleaned = cleaned.lstrip("/")
        if cleaned.startswith("output/"):
            cleaned = cleaned[len("output/"):]
        relative = Path(cleaned) if cleaned else Path(".")

    full_path = (BASE_OUTPUT_DIR / relative).resolve()
    if not str(full_path).startswith(str(BASE_OUTPUT_DIR)):
        raise ValueError("Path escapes the ./output directory")
    return full_path


@tool("Create File")
def create_file_tool(file_path: str, content: str) -> str:
    """
    Create a new file with the specified content.
    Use this tool to create any type of file (HTML, CSS, JavaScript, JSON, etc.)

    Args:
        file_path: Relative path where the file should be created (e.g., 'src/App.jsx')
        content: The complete content to write to the file

    Returns:
        Success message with file path

    Example:
        create_file_tool('src/components/Header.jsx', '<code here>')
    """
    try:
        full_path = _resolve_output_path(file_path)

        # Create parent directories if they don't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

        file_size = len(content)
        return f"✓ Successfully created file: {file_path} ({file_size} bytes)"

    except Exception as e:
        return f"✗ Error creating file {file_path}: {str(e)}"


@tool("Read File")
def read_file_tool(file_path: str) -> str:
    """
    Read the content of an existing file.
    Use this to check what's already been created or to read reference files.

    Args:
        file_path: Relative path to the file to read

    Returns:
        File content or error message

    Example:
        read_file_tool('src/App.jsx')
    """
    try:
        full_path = _resolve_output_path(file_path)

        if not full_path.exists():
            return f"✗ File not found: {file_path}"

        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return content

    except Exception as e:
        return f"✗ Error reading file {file_path}: {str(e)}"


@tool("List Directory")
def list_directory_tool(directory_path: str = ".") -> str:
    """
    List all files and directories in the specified directory.
    Use this to see what files exist in the project.

    Args:
        directory_path: Relative path to directory (default: root)

    Returns:
        List of files and directories

    Example:
        list_directory_tool('src/components')
    """
    try:
        full_path = _resolve_output_path(directory_path)

        if not full_path.exists():
            return f"✗ Directory not found: {directory_path}"

        if not full_path.is_dir():
            return f"✗ Not a directory: {directory_path}"

        items = []
        for item in sorted(full_path.iterdir()):
            item_type = "DIR " if item.is_dir() else "FILE"
            relative_path = item.relative_to(BASE_OUTPUT_DIR)
            items.append(f"{item_type} {relative_path}")

        if not items:
            return f"Directory {directory_path} is empty"

        return "\n".join(items)

    except Exception as e:
        return f"✗ Error listing directory {directory_path}: {str(e)}"


@tool("Create Directory")
def create_directory_tool(directory_path: str) -> str:
    """
    Create a new directory structure.
    Use this to set up the project folder structure.

    Args:
        directory_path: Relative path for the new directory

    Returns:
        Success message

    Example:
        create_directory_tool('src/components')
    """
    try:
        full_path = _resolve_output_path(directory_path)

        full_path.mkdir(parents=True, exist_ok=True)

        return f"✓ Successfully created directory: {directory_path}"

    except Exception as e:
        return f"✗ Error creating directory {directory_path}: {str(e)}"
