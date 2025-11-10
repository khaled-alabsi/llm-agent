# Compact Prompt: Coder Agent (LLM Tool‑Calling)

Build a lightweight coder agent that uses an OpenAI‑compatible local LLM with tool‑calling to generate small projects inside an isolated workspace.

Goal
- Implement a single‑agent loop that can plan, create files, and run simple shell commands to produce runnable projects from a short brief.

Constraints
- No agent frameworks (e.g., Azure Agent Framework, CrewAI). Use plain Python.
- Deterministic behavior: no hidden fallbacks; surface errors explicitly.
- Imports must not be wrapped in try/except.
- Config must be YAML‑backed.
- All file operations must remain inside the active project workspace.

Stack and dependencies
- Python 3.9+ with minimal deps: requests, pyyaml.

Required structure
- core/: agent orchestration and configuration
  - agent.py: ToolCallingAgent + CoderAgent (chat loop; tool registration; skill/context injection)
  - config.py: YAML config loader with defaults; prepares log directory
  - context_loader.py: load_context (excludes context/skills/), load_skills(names)
- tools/: callable tools exposed to the LLM
  - filesystem.py: write_file, read_file, list_files, describe_workspace
  - runner.py: run_shell (non‑interactive bash within workspace)
- helpers/: shared utilities
  - file_utils.py: Workspace with safe path resolution (supports absolute paths inside root), string‑only write_file content
  - logger.py: basic logger factory
- context/: knowledge base
  - skills/: skill blueprints (e.g., coder, react_js, personal_website)
  - nogo/: non‑negotiable rules (e.g., no_svg)
- logs/: session logs (jsonl + pretty JSON), one file per session in order
- generated_projects/: output workspaces (gitignored but tracked via placeholder)
- agent.py (repo root): thin entry that instantiates CoderAgent and triggers a sample build
- agent_ui.ipynb: notebook with cells for config, skills selection, build, inspect, runner‑tool test, and log viewing

Agent behavior
- Accepts a brief and optional skills list; merges base skills (coder) with the provided list.
- Builds a system message from context plus skills; uses OpenAI tool‑calling to decide when to call tools.
- Executes tool calls, appends results, and iterates until a final answer or iteration cap.
- If the LLM stops with `finish_reason: length`, automatically compacts the chat history using an LLM‑powered history tool that operates ONLY on chat messages (never on tool definitions), then retries with the compacted history.
  - Compaction summarizes only the "head" via LLM; the last N messages (the "tail") are appended programmatically and preserved verbatim. Tool definitions are always excluded from the summarization prompt.

Tools and safety
- write_file: requires string content; respects overwrite flag; rejects paths outside workspace.
- read_file, list_files, describe_workspace: enable inspection.
- run_shell: runs safe, non‑interactive commands in the workspace; supports relative cwd.
- summarize_history (internal): LLM‑powered tool that compresses earlier conversation while keeping the last messages intact; returns a compact `messages` array. Tool definitions are excluded from the summarization request.

Logging
- Maintain a single aggregate pretty log at `logs/agent.log.json` (append‑only array).
- For each run, also create a session folder under `logs/sessions/session_{index}_{timestamp}/` with:
  - `session.log.json` — session‑only log in order
  - `tools/` — per‑tool I/O snapshots: one input file and one output file per tool call (including history compaction input/output)

Notebook expectations
- Configuration cell (`LLMConfig.load()`), override base_url/model/log_dir as needed.
- Instantiate `CoderAgent`, set `skills = [ ... ]`, set `project_brief`, call `build_project`.
- Cells to list files, peek at a file, test runner tool, and display session logs.

Quality
- Minimal dependencies and clear separation of concerns.
- Deterministic errors; no silent coercion or fallbacks.
- YAML for config; no prompts/ directory reliance.

Output
- Provide a concise summary with run instructions for the generated project.
