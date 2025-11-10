# Project Documentation Index

Welcome! This index is the first stop for anyone extending or operating the coder agent. Use it to navigate the repository quickly.

## Folder Overview

- `core/` – Agent orchestration, YAML-driven LLM configuration, and context loading utilities.
  - See `docs/architecture.md` for a layered overview and how to swap LLMs.
- `tools/` – Functions the agent can call (`filesystem`, `runner`, `history`).
- `helpers/` – Shared utilities such as logging and filesystem wrappers.
- `context/` – Knowledge base files automatically injected into the system prompt.
  - `context/skills/` – Task‑specific skills (blueprints) included via the notebook skills list.
- `logs/` –
  - Aggregate: `logs/agent.log.json` (single pretty JSON array of all entries, in order)
  - Per-session: `logs/sessions/session_{index}_{ts}/session.log.json` plus `tools/` with one JSON per tool call (combined input + output)
- `generated_projects/` – Output workspaces for generated apps (ignored by git, keep `.gitkeep`).
- `docs/` – Documentation hub (you are here).
  - `PROJECT_REQUIREMENTS.md` – Compact prompt that specifies how to (re)build this coder agent from scratch.
  - `architecture.md` – Architecture and responsibilities of each layer.

## Getting Started

- Create/activate `.venv` and install deps: `pip install -r requirements.txt`.
- Ensure an OpenAI‑compatible endpoint is available (default `http://localhost:1234/v1`) or update `core/config.yaml` (`base_url`, `model`, optional `api_key`).
- Run `python agent.py` or open `agent_ui.ipynb` for an interactive loop.

## Key Behaviors

- Tool‑calling: the agent registers filesystem and shell tools and lets the LLM invoke them.
- History compaction: on `finish_reason: length`, compacts the head via the `history` tool (function‑calling) and appends the tail programmatically (keeps last N messages). Tools are excluded from the summarization prompt.
- Tool summaries: summaries rewrite bulky `'tool'` role outputs into short outcome statements (files created/modified, size, status); no raw code/JSON in summaries.
- Redaction: large payloads (e.g., `write_file.content`) are redacted in assistant tool_calls and in tool‑call args within history; `path` and `description` are retained.
- Descriptive writes: `write_file` supports an optional `description` used to keep history compact.

## Notebook Tips

- Use the “Skills selection” cell to include items from `context/skills/` (e.g., `coder`, `react_js`, `personal_website`).
- The log viewer prints entries from `logs/agent.log.json`. Per-session details and per‑tool I/O are under `logs/sessions/`.

## Updating This Index

- Add links to new documents or specs when you create them.
- Keep folder descriptions current so new developers and agents can orient themselves without guesswork.
