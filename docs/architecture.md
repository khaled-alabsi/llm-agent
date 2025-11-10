# Architecture Overview

This project is a lightweight, tool-calling coder agent structured for clarity and swap‑ability.

Layers
- Core
  - `core/llm.py` — LLMClient abstraction that talks to an OpenAI‑compatible `/chat/completions` API. All HTTP and headers live here. Switching from a local server to remote OpenAI only requires YAML changes.
  - `core/agent.py` — Agent loop (ToolCallingAgent + CoderAgent). Builds system messages from context + skills, sanitizes assistant tool_calls (redacts large `content`), logs sessions, registers tools, and delegates chat calls to `LLMClient`.
  - `core/config.py` — YAML‑backed configuration loader (`core/config.yaml`). Supports `base_url`, `model`, `temperature`, `max_tokens`, `log_dir`, and optional `provider`/`api_key`.
  - `core/context_loader.py` — Loads general context and named skills (`context/skills/`), skipping the skills subtree in general context to avoid duplication.
- Tools
  - `tools/filesystem.py` — `write_file` (with optional `description` for compact history), `read_file`, `list_files`, `describe_workspace`.
  - `tools/runner.py` — `run_shell` for non‑interactive bash commands within the workspace.
  - `tools/history.py` — Summarizes earlier chat history via function‑calling; summaries rewrite bulky `'tool'` outputs into outcomes; tail is appended in code.
- Helpers
  - `helpers/file_utils.py` — `Workspace` sandbox (safe path resolution, string‑only writes).
  - `helpers/logger.py` — Logger factory.
- Context
  - `context/skills/` — Skill blueprints (`coder`, `react_js`, `personal_website`, ...).
  - `context/nogo/` — Non‑negotiable rules (e.g., `no_svg`).
- Logs
  - Aggregate: `logs/agent.log.json` — single pretty JSON array of all entries.
  - Per-session: `logs/sessions/session_{index}_{ts}/session.log.json` plus `tools/tool_###_{name}.json` (combined input + output for each tool call).

Flow
1. Notebook or entry script sets up `LLMConfig` and `CoderAgent`.
2. `CoderAgent.build_project()` merges skills, creates a workspace, and kicks off the chat loop.
3. The agent calls `LLMClient.chat()` for assistant responses; assistant tool_calls are sanitized (large payloads redacted). Tool calls are executed locally and summarized compactly.
4. Logs are written in order to `logs/agent.log.json` and the active session folder; each tool call has a single JSON file with both input and output.

Swap the LLM
- Update `core/config.yaml` with a new `base_url` and `api_key` (and optionally `provider`). No code change needed.
- If your provider deviates from OpenAI’s payload shape, add a tiny adapter in `core/llm.py`.

History Compaction
- Trigger: `finish_reason: length` with no tool_calls.
- Behavior: summarize the head via a function‑calling tool; append tail (last N messages) programmatically.
- Constant: `core/agent.py:12` defines `HISTORY_KEEP_LAST_N`.
