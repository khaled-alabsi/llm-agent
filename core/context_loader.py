"""Load reference context files for the coder agent."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


def load_context(context_dir: str | Path) -> str:
    """Concatenate readable context files to prime the agent."""

    context_path = Path(context_dir)
    if not context_path.exists():
        return ""

    parts: list[str] = []
    for file_path in sorted(_iter_context_files(context_path)):
        parts.append(f"## {file_path.name}\n")
        parts.append(file_path.read_text(encoding="utf-8"))
        parts.append("\n")
    return "\n".join(parts).strip()


def _iter_context_files(context_path: Path) -> Iterable[Path]:
    for file_path in context_path.rglob("*"):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in {".md", ".txt"}:
            continue
        yield file_path
