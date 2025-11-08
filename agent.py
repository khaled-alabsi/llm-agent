# app.py
import os
import asyncio
from functools import lru_cache
from typing import Any, Callable, Iterable

from agent_framework.core.tools import tool
from agent_framework.openai import OpenAIChatClient
from pydantic import BaseModel

# --- Env defaults for LM Studio ---
os.environ.setdefault("OPENAI_BASE_URL", "http://127.0.0.1:1234/v1")
os.environ.setdefault("OPENAI_API_KEY", "lm-studio")
os.environ.setdefault("OPENAI_CHAT_MODEL_ID", "qwen/qwen3-coder-30b")

DEFAULT_AGENT_NAME = "RepoHelper"
DEFAULT_AGENT_INSTRUCTIONS = (
    "You are a meticulous code assistant. "
    "Read the provided context, suggest concrete improvements, "
    "and when code changes are needed return a unified diff wrapped "
    "in the Patch response format."
)
DEFAULT_AGENT_TEMPERATURE = 0.2


@tool
def grep_py_functions(code: str) -> list[str]:
    """Return function defs (names) from Python code."""
    import re

    return re.findall(r"def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", code)


class Patch(BaseModel):
    filename: str
    summary: str
    diff: str


__all__ = [
    "Patch",
    "create_repo_helper_agent",
    "get_repo_helper_agent",
    "run_repo_helper",
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
    selected_tools = list(tools) if tools is not None else [grep_py_functions]
    return client.create_agent(
        name=name,
        instructions=instructions,
        tools=selected_tools,
        temperature=temperature,
        response_format=Patch,
    )


@lru_cache(maxsize=1)
def get_repo_helper_agent() -> Any:
    """
    Lazily create and cache the RepoHelper agent for reuse (e.g., notebooks).
    """
    return create_repo_helper_agent()


async def run_repo_helper(task: str, agent: Any | None = None) -> Patch:
    """
    Convenience helper that ensures the agent exists and runs the given task.
    """
    selected_agent = agent or get_repo_helper_agent()
    return await selected_agent.run(task)


async def main():
    """
    Minimal CLI entry point for manual testing.
    """
    user_task = (
        "Read agent.py, summarize the RepoHelper design, "
        "and suggest one improvement."
    )
    result = await run_repo_helper(user_task)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
