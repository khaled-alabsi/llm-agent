# Project Documentation Index

Welcome! This index is the first stop for anyone extending or operating the coder agent. Use it to navigate the repository quickly.

## Folder Overview

- `core/` – Agent orchestration, YAML-driven LLM configuration, and context loading utilities.
- `tools/` – Functions the agent can call (currently filesystem helpers).
- `helpers/` – Shared utilities such as logging and filesystem wrappers.
- `context/` – Knowledge base files automatically injected into the system prompt.
- `prompts/` – Prompt templates that define how the agent tackles tasks.
- `logs/` – JSON request/response traces (ignored by git, keep for debugging).
- `generated_projects/` – Output workspaces for generated apps (ignored by git, keep `.gitkeep`).
- `docs/` – Documentation hub (you are here).

## Getting Started

1. Create/activate the `.venv` virtual environment in the repo root.
2. Install dependencies with `pip install -r requirements.txt`.
3. Ensure your local LLM endpoint (e.g., LM Studio) is running on `http://localhost:1234/v1` or update `core/config.yaml` accordingly.
4. Run `python agent.py` or use `agent_ui.ipynb` for an interactive build loop.

## Updating This Index

- Add links to new documents or specs when you create them.
- Keep folder descriptions current so new developers and agents can orient themselves without guesswork.
