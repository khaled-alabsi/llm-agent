# Quick Reference Card

Fast lookup for common tasks and information.

## Project Structure at a Glance

```
llm-agent/
├── main.py                  # Run this: python main.py
├── agent_control.ipynb      # Or this: jupyter notebook agent_control.ipynb
├── config.yaml              # Edit settings here
│
├── core/                    # Agent brain
│   ├── llm_config.py       # LLM setup
│   ├── agent_factory.py    # Create agents
│   └── context_loader.py   # Load context
│
├── tools/                   # Agent tools
│   ├── file_tools.py       # File operations
│   └── code_tools.py       # Code validation
│
├── helpers/                 # Utilities
│   ├── logger.py           # Session logging
│   ├── config_loader.py    # Config management
│   └── file_utils.py       # File utilities
│
├── context/                 # Agent knowledge
│   ├── no-goes.md          # Safety rules
│   ├── guidelines/         # Best practices
│   ├── skills/             # Technical knowledge
│   └── examples/           # Reference examples
│
├── prompts/                 # Task definitions
│   └── build-website.md    # Default task
│
├── docs/                    # Documentation
│   └── index.md            # 👈 START HERE
│
├── logs/                    # Session logs
└── output/                  # Generated code
```

## Common Commands

```bash
# First time setup
pip install -r requirements.txt

# Run agent (CLI)
python main.py

# Run agent (Notebook)
jupyter notebook agent_control.ipynb

# Check output
ls -R output/

# View latest logs
ls -lt logs/ | head -5

# Clean output
rm -rf output/* (be careful!)
```

## Quick Access

### Entry Points
- **Docs**: [docs/index.md](index.md)
- **Requirements**: [PROJECT_REQUIREMENTS.md](../PROJECT_REQUIREMENTS.md)
- **README**: [README.md](../README.md)

### Key Configuration
```yaml
# config.yaml
llm:
  base_url: "http://localhost:1234/v1"  # LM Studio
  model: "qwen/qwen3-coder-30b"         # Model name
  temperature: 0.7                       # Creativity
  max_tokens: 4000                       # Response length

agent:
  max_iterations: 25                     # Tool call limit
```

### Important Paths
- **Config**: `config.yaml`
- **Prompt**: `prompts/build-website.md`
- **No-goes**: `context/no-goes.md`
- **Logs**: `logs/session_*.log` and `logs/session_*.json`
- **Output**: `output/`

## Task → Doc Mapping

| I want to... | Read this doc |
|-------------|---------------|
| Start quickly | [Quick Start](guides/quick-start.md) |
| Add a tool | [Adding Tools](guides/adding-tools.md) |
| Understand code | [Code Structure](architecture/code-structure.md) |
| See architecture | [Architecture Overview](architecture/overview.md) |
| Configure LLM | [Configuration Guide](guides/configuration.md) |
| Debug | [Debugging Guide](development/debugging.md) |

## File Patterns

### Python Files
```python
# Import pattern
from core.llm_config import setup_llm
from helpers import get_config, SessionLogger
from tools import create_file_tool

# Tool pattern
@tool("Tool Name")
def my_tool(param: str) -> str:
    """Tool description"""
    try:
        # logic
        return "✓ Success"
    except Exception as e:
        return f"✗ Error: {e}"

# Config access
config = get_config()
value = config.get('section.key', default)

# Logging
logger = SessionLogger()
logger.log_event('type', {'data': 'value'})
logger.end_session()
```

### Tool Return Format
- Success: `"✓ Success message"`
- Error: `"✗ Error message"`
- Warning: `"⚠ Warning message"`

## Common Issues & Solutions

### LM Studio not connecting
```bash
# Check if server is running
curl http://localhost:1234/v1/models

# If fails: Start LM Studio server
# Update port in config.yaml if different
```

### Import errors
```bash
pip install -r requirements.txt --upgrade
```

### Agent not using tools
- Check tool docstring is clear
- Verify prompt explicitly asks for tool use
- Increase max_iterations in config
- Review logs to see what agent attempts

### No output generated
- Check logs/session_*.log for errors
- Verify LM Studio is responding
- Check output/ directory permissions

## File Sizes

| Component | Approx Size |
|-----------|-------------|
| Core modules | ~500 lines total |
| Tools | ~200 lines total |
| Helpers | ~400 lines total |
| Context | ~2000 lines total |
| Docs | ~3000 lines total |
| Config | ~100 lines |

## Dependencies Count

- **Total**: 13 packages
- **Core**: 5 (crewai, langchain, etc.)
- **Utils**: 4 (pyyaml, requests, etc.)
- **UI**: 2 (jupyter, ipython)
- **Display**: 2 (rich, colorama)

## Session Log Format

```
logs/
├── session_20251109_142030.log   # Human readable
└── session_20251109_142030.json  # Machine readable
```

### Log Contents
- Session start/end timestamps
- All LLM requests/responses
- All tool calls with args/results
- Errors with stack traces
- Metrics (calls, tokens, duration)

## Config Sections Quick Ref

```yaml
llm:          # LLM connection settings
agent:        # Agent behavior
tools:        # Tool configuration
output:       # Output directory
logging:      # Log settings
context:      # Context file paths
safety:       # Security settings
```

## Code Quality Checklist

- [ ] All functions have docstrings
- [ ] Type hints used
- [ ] Error handling present
- [ ] No hardcoded values
- [ ] No magic numbers
- [ ] Follows no-goes.md rules
- [ ] Tested manually

## Performance Tips

- Context loaded once per session (not per call)
- Config cached globally (singleton)
- Logs written asynchronously
- File ops sandboxed to output/
- Use max_tokens wisely

## Security Notes

- All file ops limited to `./output/`
- Paths validated before operations
- No parent directory access (`../`)
- Safety rules in context/no-goes.md
- No system-wide changes

## Extending the Agent

### Add New Tool
1. Create in `tools/my_tools.py`
2. Use `@tool()` decorator
3. Register in `core/agent_factory.py`

### Add New Context
1. Create `.md` in `context/skills/`
2. Load in `core/context_loader.py`
3. Include in `build_context_prompt()`

### Add New Prompt
1. Create `.md` in `prompts/`
2. Load with `load_prompt_template('name')`
3. Pass to task creation

## Monitoring

### Check Session Metrics
```python
import json
with open('logs/session_*.json') as f:
    data = json.load(f)
    print(data['metrics'])
```

### Output
- `total_llm_calls`: LLM API calls
- `total_tool_calls`: Tool executions
- `total_tokens`: Tokens used
- `errors`: Error count

## Version Info

- **Current Version**: 1.0.0
- **CrewAI**: >=0.41.0
- **Python**: 3.10+
- **LM Studio**: Latest

## Getting Help

1. Check [docs/index.md](index.md) for task-based navigation
2. Review [PROJECT_REQUIREMENTS.md](../PROJECT_REQUIREMENTS.md)
3. Look at logs in `logs/` directory
4. Check [Debugging Guide](development/debugging.md)

## Credits & Links

- **CrewAI**: https://docs.crewai.com/
- **LM Studio**: https://lmstudio.ai/
- **LangChain**: https://python.langchain.com/
- **Project**: [README.md](../README.md)
