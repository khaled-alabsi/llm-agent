"""Load reference context files for the coder agent."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List


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


def load_skills(skills_dir: str | Path, names: List[str]) -> str:
    """Load one or more skill documents by base name (without extension).

    Raises FileNotFoundError if any requested skill is missing to avoid
    silent fallbacks.
    """

    root = Path(skills_dir)
    if not root.exists():
        raise FileNotFoundError(f"Skills directory not found: {root}")

    def _resolve(name: str) -> Path:
        candidates = list(root.glob(f"**/{name}.md")) + list(root.glob(f"**/{name}.txt"))
        if not candidates:
            raise FileNotFoundError(f"Skill not found: {name}")
        # If multiple matches, prefer top-level match; otherwise first.
        candidates.sort(key=lambda p: (len(p.relative_to(root).parts), str(p)))
        return candidates[0]

    parts: list[str] = []
    for name in names:
        file_path = _resolve(name)
        parts.append(f"## SKILL: {file_path.stem}\n")
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
