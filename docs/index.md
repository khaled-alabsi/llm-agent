# Project Documentation Index

Welcome! This index is the first stop for anyone extending or operating the coder agent. Use it to navigate the repository quickly.

## Folder Overview

- `core/` – Agent orchestration, YAML-driven LLM configuration, and context loading utilities.
  - See `docs/architecture.md` for a layered overview and how to swap LLMs.
- `tools/` – Functions the agent can call (currently filesystem helpers).
- `helpers/` – Shared utilities such as logging and filesystem wrappers.
- `context/` – Knowledge base files automatically injected into the system prompt.
  - `context/skills/` – Task‑specific skills (blueprints) included via the notebook skills list.
- `logs/` – Single append-only pretty JSON file `agent.log.json` containing all requests/responses in order.
- `generated_projects/` – Output workspaces for generated apps (ignored by git, keep `.gitkeep`).
- `docs/` – Documentation hub (you are here).
  - `PROJECT_REQUIREMENTS.md` – Compact prompt that specifies how to (re)build this coder agent from scratch.
  - `architecture.md` – Architecture and responsibilities of each layer.

## Getting Started

1. Create/activate the `.venv` virtual environment in the repo root.
2. Install dependencies with `pip install -r requirements.txt`.
3. Ensure your local LLM endpoint (e.g., LM Studio) is running on `http://localhost:1234/v1` or update `core/config.yaml` accordingly.
4. Run `python agent.py` or use `agent_ui.ipynb` for an interactive build loop.

## Notes

- The agent writes all requests/responses of a run to a single session log file (`logs/session_*.jsonl`) and maintains a formatted companion file (`.pretty.json`).
- Use the notebook’s “Skills selection” cell to include items from `context/skills/` (e.g., `coder`, `react_js`, `personal_website`).

## Updating This Index

- Add links to new documents or specs when you create them.
- Keep folder descriptions current so new developers and agents can orient themselves without guesswork.
