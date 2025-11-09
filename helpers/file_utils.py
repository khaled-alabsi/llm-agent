"""File utility functions"""

from pathlib import Path
from typing import List, Optional


def ensure_directory(path: str) -> Path:
    """
    Ensure directory exists, create if it doesn't

    Args:
        path: Directory path

    Returns:
        Path object
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def read_markdown_file(file_path: str) -> str:
    """
    Read markdown file content

    Args:
        file_path: Path to markdown file

    Returns:
        File content as string

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Markdown file not found: {file_path}")

    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def read_text_file(file_path: str) -> str:
    """
    Read text file content

    Args:
        file_path: Path to text file

    Returns:
        File content as string
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_text_file(file_path: str, content: str):
    """
    Write content to text file

    Args:
        file_path: Path to file
        content: Content to write
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def list_files(directory: str, pattern: str = "*", recursive: bool = False) -> List[Path]:
    """
    List files in directory

    Args:
        directory: Directory path
        pattern: Glob pattern (default: all files)
        recursive: Search recursively

    Returns:
        List of Path objects
    """
    dir_path = Path(directory)

    if not dir_path.exists():
        return []

    if recursive:
        return list(dir_path.rglob(pattern))
    else:
        return list(dir_path.glob(pattern))


def get_file_size(file_path: str) -> int:
    """
    Get file size in bytes

    Args:
        file_path: Path to file

    Returns:
        File size in bytes
    """
    return Path(file_path).stat().st_size


def file_exists(file_path: str) -> bool:
    """
    Check if file exists

    Args:
        file_path: Path to file

    Returns:
        True if file exists
    """
    return Path(file_path).exists()
