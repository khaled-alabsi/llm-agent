# Architecture Overview

This project is a lightweight, tool-calling coder agent structured for clarity and swap‑ability.

Layers
- Core
  - `core/llm.py` — LLMClient abstraction that talks to an OpenAI‑compatible `/chat/completions` API. All HTTP and headers live here. Switching from a local server to remote OpenAI only requires YAML changes.
  - `core/agent.py` — Agent loop (ToolCallingAgent + CoderAgent). Builds system messages from context + skills, logs sessions, registers tools, and delegates chat calls to `LLMClient`.
  - `core/config.py` — YAML‑backed configuration loader (`core/config.yaml`). Supports `base_url`, `model`, `temperature`, `max_tokens`, `log_dir`, and optional `provider`/`api_key`.
  - `core/context_loader.py` — Loads general context and named skills (`context/skills/`), skipping the skills subtree in general context to avoid duplication.
- Tools
  - `tools/filesystem.py` — `write_file`, `read_file`, `list_files`, `describe_workspace`.
  - `tools/runner.py` — `run_shell` for non‑interactive bash commands within the workspace.
- Helpers
  - `helpers/file_utils.py` — `Workspace` sandbox (safe path resolution, string‑only writes).
  - `helpers/logger.py` — Logger factory.
- Context
  - `context/skills/` — Skill blueprints (`coder`, `react_js`, `personal_website`, ...).
  - `context/nogo/` — Non‑negotiable rules (e.g., `no_svg`).
- Logs
  - `logs/session_*.jsonl` — Append‑only session transcripts.
  - `logs/session_*.pretty.json` — Readable, fully formatted session arrays.

Flow
1. Notebook or entry script sets up `LLMConfig` and `CoderAgent`.
2. `CoderAgent.build_project()` merges skills, creates a workspace, and kicks off the chat loop.
3. The agent calls `LLMClient.chat()` for assistant responses. Tool calls are executed locally and appended to the transcript.
4. Logs are written in order to a single session file + pretty JSON.

Swap the LLM
- Update `core/config.yaml` with a new `base_url` and `api_key` (and optionally `provider`). No code change needed.
- If your provider deviates from OpenAI’s payload shape, add a tiny adapter in `core/llm.py`.

