# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

first, you should know what the user like and dont like by reading this file my-code.md

## Project Overview

This is a CrewAI-based coding agent that uses local LLMs (via LM Studio) to autonomously build complete web applications. The agent is context-aware, loading skills, guidelines, and safety rules to generate production-ready code.

**Key Purpose**: Educational project demonstrating agent architecture, tool usage, and LLM response handling.

## Running the Agent

### Prerequisites
LM Studio must be running with a model loaded (default: Qwen3-Coder-30B) at `http://localhost:1234`

### Execute Agent
```bash
# CLI execution
python main.py

# Interactive notebook
jupyter notebook agent_control.ipynb

# Install dependencies first if needed
pip install -r requirements.txt
```

### Check Results
- Generated code: `./output/`
- Session logs: `./logs/session_YYYYMMDD_HHMMSS.log` and `.json`

## Architecture: The Big Picture

### Critical Design Pattern: Context Injection
The agent's behavior is NOT hardcoded - it's controlled by markdown files in `context/`:

1. **Safety Rules** (`context/no-goes.md`) - Absolute prohibitions that MUST be followed
2. **Skills** (`context/skills/`) - Technical knowledge (React, web dev patterns)
3. **Guidelines** (`context/guidelines/`) - Coding standards and best practices
4. **Examples** (`context/examples/`) - Reference implementations

These are loaded by `core/context_loader.py` and injected into the agent's backstory during initialization. This is the PRIMARY way to control agent behavior - not by modifying core code.

### Data Flow: Initialization → Execution

```
main.py
  ├─> Load config.yaml (singleton via helpers/config_loader.py)
  ├─> Create SessionLogger (one file per run)
  └─> create_coder_crew()
       ├─> setup_llm() - Connects to LM Studio
       ├─> load_context_files() - Loads all context/*.md files
       ├─> build_context_prompt() - Merges into single backstory
       └─> create_coder_agent()
            ├─> CrewAI Agent with enhanced backstory
            └─> Registers 6 tools (file ops, code validation)

crew.kickoff()
  └─> Agent iterates (max 25 times by default):
       1. Calls LLM with task + tool schemas
       2. LLM responds with tool_calls JSON
       3. Agent executes tools (sandboxed to ./output/)
       4. Results sent back to LLM
       5. Repeat until task complete
```

### Module Responsibilities

**core/**: Agent orchestration
- `llm_config.py` - LangChain ChatOpenAI setup for LM Studio
- `agent_factory.py` - Creates agents/crews, injects context
- `context_loader.py` - Loads and merges all context files

**tools/**: CrewAI @tool decorated functions
- `file_tools.py` - create_file, read_file, list_directory, create_directory
- `code_tools.py` - format_code, validate_json
- All return strings: "✓ Success", "✗ Error", "⚠ Warning"

**helpers/**: Utilities (no business logic)
- `logger.py` - SessionLogger class (one .log + .json per session)
- `config_loader.py` - YAML config with dot-notation access
- `file_utils.py` - File system helpers

**context/**: Agent knowledge (markdown files)
- Loaded once per session, injected into agent backstory
- This is where you control agent behavior

### The Singleton Pattern: Config Access
```python
from helpers import get_config

config = get_config()  # Always returns same instance
model = config.get('llm.model')  # Dot-notation access
```

### The Session Pattern: Logging
```python
from helpers.logger import SessionLogger

logger = SessionLogger()  # Creates session_YYYYMMDD_HHMMSS.{log,json}
logger.log_llm_call(request, response, duration)
logger.log_tool_call(name, args, result, duration)
logger.end_session()  # Saves final metrics
```

## Critical Safety Rules (context/no-goes.md)

When generating code or using tools:
- **NEVER generate SVG/PNG** - use placeholder text or TODOs
- **NEVER operate outside ./output/** - all file operations sandboxed
- **NEVER hardcode credentials** - no API keys, passwords, secrets
- **ALWAYS include error handling** - try/catch everywhere
- **ALWAYS use named constants** - no magic numbers
- **ALWAYS document** - docstrings required

These rules are loaded from `context/no-goes.md` and injected into the agent. When working on this codebase, you must follow them too.

## Adding New Functionality

### Add a Tool (most common task)
1. Create function in `tools/my_tools.py`:
```python
from crewai.tools import tool

@tool("Tool Name")
def my_tool(param: str) -> str:
    """Clear description - agent reads this to decide when to use."""
    try:
        # Logic here
        return "✓ Success: result"
    except Exception as e:
        return f"✗ Error: {e}"
```

2. Register in `core/agent_factory.py` in `create_coder_agent()`:
```python
from tools.my_tools import my_tool

agent = Agent(
    tools=[
        create_file_tool,
        # ... existing tools ...
        my_tool,  # Add here
    ]
)
```

### Add Context (to change agent behavior)
1. Create `context/skills/my-skill.md` or `context/guidelines/my-guideline.md`
2. Load in `core/context_loader.py`:
```python
def load_context_files():
    context = {}
    # ... existing loads ...
    context['my_skill'] = read_markdown_file('context/skills/my-skill.md')
    return context
```
3. Include in `build_context_prompt()` to inject into agent

### Add a New Prompt Template
1. Create `prompts/my-task.md` with task description
2. Load with: `load_prompt_template('my-task')`
3. Pass to `create_website_task(agent, prompt_override=prompt)`

## Configuration (config.yaml)

Key settings to adjust:
```yaml
llm:
  base_url: "http://localhost:1234/v1"  # LM Studio endpoint
  model: "qwen/qwen3-coder-30b"         # Change model here
  temperature: 0.7                       # Creativity level
  max_tokens: 4000                       # Response length

agent:
  max_iterations: 25  # Tool call limit (prevents infinite loops)

output:
  directory: "./output"  # Generated code goes here (sandboxed)

logging:
  log_tool_calls: true      # Log every tool execution
  log_llm_responses: true   # Log full request/response
```

Access in code: `config.get('llm.model')` or `config.get_section('agent')`

## Debugging

### Check Logs
```bash
# Latest session log (human-readable)
ls -t logs/*.log | head -1 | xargs cat

# Latest session metrics (JSON)
ls -t logs/*.json | head -1 | xargs cat | jq '.metrics'
```

### Common Issues

**Agent not using tools**: Tool docstring unclear or prompt doesn't request action
- Fix: Improve tool description, make prompt more explicit

**LM Studio connection failed**: Server not running or wrong port
- Test: `curl http://localhost:1234/v1/models`

**File operations fail**: Trying to write outside ./output/
- Check: File paths in tools are validated in `tools/file_tools.py`

**Context not loading**: Markdown files missing or path wrong
- Check: `core/context_loader.py` file paths

## Testing Changes

No automated tests currently. Manual testing:
1. Modify code
2. Run `python main.py`
3. Check `logs/session_*.log` for execution details
4. Verify `output/` contains expected generated files

## Documentation Reference

**For detailed guidance**, see `docs/index.md` - task-based navigation to specific docs:
- Architecture deep-dive: `docs/architecture/code-structure.md`
- Adding tools guide: `docs/guides/adding-tools.md`
- Complete requirements: `PROJECT_REQUIREMENTS.md`

## Key Files Quick Reference

- `config.yaml` - All configurable settings
- `main.py` - CLI entry point
- `core/agent_factory.py` - Where agents are created and tools registered
- `core/context_loader.py` - Where context files are loaded
- `context/no-goes.md` - Safety rules (critical to read)
- `tools/file_tools.py` - Most commonly extended
- `logs/session_*.{log,json}` - Debugging information

## Import Patterns

Always use absolute imports:
```python
from core.llm_config import setup_llm
from helpers import get_config, SessionLogger
from tools import create_file_tool
```

Never use relative imports like `from ..core import`.

## Tool Return Format Convention

All tools must return strings in this format:
- Success: `"✓ Success message with details"`
- Error: `"✗ Error: specific error description"`
- Warning: `"⚠ Warning: what went wrong"`

The agent parses these symbols to understand results.

## Output Sandboxing

**Critical**: All file operations are restricted to `./output/` via path validation in `tools/file_tools.py`:
```python
base_dir = Path("./output")
full_path = base_dir / file_path  # Always prefixed with ./output
```

Never remove this sandboxing - it's a core safety feature.
