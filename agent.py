"""Entry point for running the coder agent demo."""

from core.agent import CoderAgent, ToolCallingAgent  # noqa: F401
from core.config import LLMConfig  # noqa: F401

if __name__ == "__main__":
    agent = CoderAgent()
    example_brief = (
        "Create a minimal task-tracking CLI. It should save tasks to a JSON file and "
        "support adding, listing, and completing tasks. Provide a README with usage."
    )
    print(agent.build_project(example_brief, project_name="task_cli", max_iterations=6))
