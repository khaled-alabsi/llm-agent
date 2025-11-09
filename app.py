import os
import asyncio
from functools import lru_cache
from typing import Any, Callable, Iterable
from agent_framework.openai import OpenAIChatClient
from pydantic import BaseModel, Field

# --- Env defaults for LM Studio ---
os.environ.setdefault("OPENAI_BASE_URL", "http://127.0.0.1:1234/v1")
os.environ.setdefault("OPENAI_API_KEY", "lm-studio")
os.environ.setdefault("OPENAI_CHAT_MODEL_ID", "qwen/qwen3-coder-30b")

# --- Project output directory ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DEFAULT_AGENT_NAME = "RepoHelper"
DEFAULT_AGENT_INSTRUCTIONS = (
    "You are a meticulous code assistant.\n"
    "- When asked to implement code or create project files, you MUST write actual files using the write_file(filename, content) tool.\n"
    "- For each file, include complete file contents (no placeholders) and call write_file once per file.\n"
    "- Normalize target paths to the /output directory. If the user mentions '/output/...' or 'output/...', write to that filename in /output.\n"
    "- After writing all files, call list_output() to verify the files exist.\n"
    "- When only suggesting improvements (no file creation), output a unified diff wrapped in the Patch format."
)
DEFAULT_AGENT_TEMPERATURE = 0.2


# ---------------------------------------------------------------------------
# Structured Output Model
# ---------------------------------------------------------------------------

class Patch(BaseModel):
    """
    Represents a structured response from the repo agent.

    Fields:
        filename (str): Path or name of the file primarily affected.
        summary (str): Short description of the change.
        diff (str): Unified diff or patch text representing the change.
    """
    filename: str = Field(..., description="Path of the file or module changed")
    summary: str = Field(..., description="Short description of the change")
    diff: str = Field(..., description="Unified diff of the change")


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

def _normalize_to_output(filename: str) -> str:
    """
    Map any of: 'main.py', 'output/main.py', '/output/main.py' to a safe path
    within OUTPUT_DIR. Prevent directory traversal.
    """
    name = filename.strip().lstrip("/")  # drop leading slash
    if name.startswith("output/"):
        name = name[len("output/"):]
    # Disallow path traversal
    safe_rel = os.path.normpath(name)
    if safe_rel.startswith(".."):
        raise ValueError("Invalid filename (path traversal).")
    return os.path.join(OUTPUT_DIR, safe_rel)

def write_file(filename: str, content: str) -> str:
    """
    Save content into the /output directory. Accepts 'main.py', 'output/main.py',
    or '/output/main.py'. Creates parent directories as needed.
    Returns the absolute path of the written file.
    """
    print(f"calling write_file with filename={filename}")
    target_path = _normalize_to_output(filename)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"write_file completed successfully: {target_path}")
    return f"File written successfully: {target_path}"

def list_output() -> list[str]:
    """
    Return a list of files currently present under /output (relative paths).
    Useful for the agent to verify file creation.
    """
    results = []
    for root, _, files in os.walk(OUTPUT_DIR):
        for fn in files:
            abs_p = os.path.join(root, fn)
            rel = os.path.relpath(abs_p, BASE_DIR)
            results.append(rel)
    results.sort()
    return results

def grep_py_functions(code: str) -> list[str]:
    """Return function defs (names) from Python code."""
    import re
    return re.findall(r"def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", code)


# ---------------------------------------------------------------------------
# Agent factory and runner
# ---------------------------------------------------------------------------

__all__ = [
    "Patch",
    "create_repo_helper_agent",
    "get_repo_helper_agent",
    "run_repo_helper",
    "write_file",
    "list_output",
]

def create_repo_helper_agent(
    *,
    name: str = DEFAULT_AGENT_NAME,
    instructions: str = DEFAULT_AGENT_INSTRUCTIONS,
    temperature: float = DEFAULT_AGENT_TEMPERATURE,
    tools: Iterable[Callable] | None = None,
) -> Any:
    """
    Factory for a RepoHelper agent wired to the local LM Studio endpoint.
    """
    client = OpenAIChatClient()
    selected_tools = list(tools) if tools is not None else [
        write_file,      # must be first to encourage tool usage
        list_output,
        grep_py_functions,
    ]
    return client.create_agent(
        name=name,
        instructions=instructions,
        tools=selected_tools,
        temperature=temperature,
        response_format=Patch,
    )

@lru_cache(maxsize=1)
def get_repo_helper_agent() -> Any:
    """Lazily create and cache the RepoHelper agent."""
    return create_repo_helper_agent()

async def run_repo_helper(task: str, agent: Any | None = None) -> Patch:
    """
    Run a task through the RepoHelper agent and return a validated Patch model.
    """
    selected_agent = agent or get_repo_helper_agent()
    resp = await selected_agent.run(task)

    if getattr(resp, "value", None) is not None:
        return resp.value  # Pydantic model (Patch)

    raise ValueError(
        "Structured response missing. Model returned plain text instead of Patch. "
        "Inspect resp.text for details."
    )

async def main():
    """
    Manual test entry point.
    You can ask the agent to create files inside /output.
    """
    user_task = (
        "Create a simple Python project in the /output directory: "
        "main.py prints 'Hello from RepoHelper!', utils.py has greet(name)->str, "
        "and README.md explains how to run it. Write the files using write_file, "
        "then call list_output to confirm."
    )
    result = await run_repo_helper(user_task)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
