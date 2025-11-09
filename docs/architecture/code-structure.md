# Code Structure

Complete guide to the codebase organization.

## Directory Structure

```
llm-agent/
├── config.yaml              # Configuration
├── main.py                  # CLI entry point
├── agent_control.ipynb      # Jupyter UI
├── requirements.txt         # Python dependencies
│
├── core/                    # Core agent logic
│   ├── __init__.py
│   ├── llm_config.py       # LLM setup (LM Studio)
│   ├── agent_factory.py    # Agent/crew creation
│   └── context_loader.py   # Load context files
│
├── tools/                   # CrewAI tools
│   ├── __init__.py
│   ├── file_tools.py       # File CRUD operations
│   └── code_tools.py       # Code validation
│
├── helpers/                 # Utility modules
│   ├── __init__.py
│   ├── logger.py           # Session logging
│   ├── config_loader.py    # YAML config
│   └── file_utils.py       # File utilities
│
├── context/                 # Agent knowledge
│   ├── no-goes.md          # Safety rules
│   ├── guidelines/         # Coding standards
│   ├── skills/             # Technical knowledge
│   └── examples/           # Reference examples
│
├── prompts/                 # Task definitions
│   └── build-website.md
│
├── logs/                    # Session logs
└── output/                  # Generated code
```

## Module Overview

### Core Modules

#### `core/llm_config.py`
**Purpose**: Configure LangChain to work with LM Studio

**Key Functions**:
- `setup_llm()` - Creates ChatOpenAI instance for LM Studio

**Usage**:
```python
from core.llm_config import setup_llm
llm = setup_llm()  # Returns configured LLM
```

#### `core/agent_factory.py`
**Purpose**: Create and configure CrewAI agents and crews

**Key Functions**:
- `create_coder_agent(llm, verbose)` - Create developer agent
- `create_website_task(agent, prompt)` - Create task
- `create_coder_crew(custom_prompt, verbose)` - Create complete crew

**Usage**:
```python
from core.agent_factory import create_coder_crew
crew = create_coder_crew()
result = crew.kickoff()
```

#### `core/context_loader.py`
**Purpose**: Load and manage context files

**Key Functions**:
- `load_context_files()` - Load all context
- `build_context_prompt(context)` - Build prompt from context
- `load_prompt_template(name)` - Load task prompt

**Usage**:
```python
from core.context_loader import load_context_files
context = load_context_files()
```

### Tools Modules

#### `tools/file_tools.py`
**Purpose**: File operation tools for the agent

**Tools**:
- `create_file_tool(path, content)` - Create file
- `read_file_tool(path)` - Read file
- `list_directory_tool(path)` - List directory
- `create_directory_tool(path)` - Create directory

**Usage**:
```python
from tools.file_tools import create_file_tool
result = create_file_tool('src/App.jsx', code_content)
```

#### `tools/code_tools.py`
**Purpose**: Code validation and formatting

**Tools**:
- `format_code_tool(code, language)` - Format code
- `validate_json_tool(json_string)` - Validate JSON

### Helper Modules

#### `helpers/logger.py`
**Purpose**: Session-based logging system

**Key Class**: `SessionLogger`

**Methods**:
- `log_event(type, data)` - Log an event
- `log_llm_call(request, response, duration)` - Log LLM call
- `log_tool_call(name, args, result, duration)` - Log tool execution
- `log_error(type, message, context)` - Log error
- `end_session()` - Save final logs

**Usage**:
```python
from helpers.logger import SessionLogger
logger = SessionLogger()
logger.log_event('custom_event', {'data': 'value'})
logger.end_session()
```

#### `helpers/config_loader.py`
**Purpose**: YAML configuration management

**Key Class**: `ConfigLoader`

**Methods**:
- `get(key_path, default)` - Get config value by dot notation
- `get_section(section)` - Get entire section
- `reload()` - Reload from file

**Usage**:
```python
from helpers.config_loader import load_config, get_config
config = load_config()
model = config.get('llm.model')
```

#### `helpers/file_utils.py`
**Purpose**: File system utilities

**Functions**:
- `ensure_directory(path)` - Create directory if needed
- `read_markdown_file(path)` - Read markdown
- `write_text_file(path, content)` - Write text file
- `list_files(dir, pattern, recursive)` - List files
- `file_exists(path)` - Check file existence

## Data Flow

### 1. Initialization Flow
```
main.py
  → load_config() [helpers/config_loader.py]
  → SessionLogger() [helpers/logger.py]
  → create_coder_crew() [core/agent_factory.py]
      → setup_llm() [core/llm_config.py]
      → load_context_files() [core/context_loader.py]
      → create_coder_agent()
          → Agent() [CrewAI]
          → register tools [tools/]
```

### 2. Execution Flow
```
crew.kickoff()
  → Agent processes task
  → Agent calls LLM
      → logger.log_llm_call()
  → LLM responds with tool calls
  → Agent executes tools
      → create_file_tool()
      → logger.log_tool_call()
  → Agent continues until task complete
  → Return result
```

### 3. Logging Flow
```
SessionLogger
  → log_event()
      → Append to session_data['events']
      → Write to .log file
      → Save to .json file
  → end_session()
      → Calculate metrics
      → Save final logs
```

## Key Design Patterns

### 1. Factory Pattern
**Where**: `core/agent_factory.py`

**Why**: Centralizes agent/crew creation logic

**Example**:
```python
# Instead of creating agents directly everywhere
agent = create_coder_agent()  # Factory handles complexity
```

### 2. Singleton Config
**Where**: `helpers/config_loader.py`

**Why**: Single config instance across application

**Example**:
```python
config = get_config()  # Always returns same instance
```

### 3. Session Pattern
**Where**: `helpers/logger.py`

**Why**: One log file per execution session

**Example**:
```python
logger = SessionLogger(session_id='unique_id')
# All logs go to same session file
logger.end_session()
```

### 4. Decorator Tools
**Where**: `tools/*.py`

**Why**: CrewAI's tool registration pattern

**Example**:
```python
@tool("Tool Name")
def my_tool(param: str) -> str:
    return result
```

## Extension Points

### Adding New Tools
1. Create function in `tools/`
2. Decorate with `@tool()`
3. Register in `core/agent_factory.py`
4. See: [Adding Tools Guide](../guides/adding-tools.md)

### Adding New Agents
1. Create agent function in `core/agent_factory.py`
2. Define role, goal, backstory
3. Assign tools
4. See: [Creating Agents Guide](../guides/creating-agents.md)

### Adding Context
1. Create `.md` file in `context/`
2. Load in `core/context_loader.py`
3. Include in `build_context_prompt()`

### Custom Logging
1. Extend `SessionLogger` class
2. Add custom `log_*` methods
3. Use in your code

## File Naming Conventions

### Python Files
- `snake_case.py` for modules
- `__init__.py` for packages
- Single responsibility per file

### Context Files
- `kebab-case.md` for markdown
- Descriptive names (e.g., `coding-standards.md`)
- Organized by type (skills/, guidelines/, examples/)

### Log Files
- `session_YYYYMMDD_HHMMSS.log` - Text log
- `session_YYYYMMDD_HHMMSS.json` - Structured data
- One per execution

## Import Structure

### Absolute Imports (Preferred)
```python
from core.llm_config import setup_llm
from helpers.logger import SessionLogger
from tools.file_tools import create_file_tool
```

### Package Imports
```python
from helpers import SessionLogger, load_config
from tools import create_file_tool, read_file_tool
```

## Dependencies

### External Dependencies
- `crewai` - Agent framework
- `langchain-openai` - LLM integration
- `pyyaml` - Config files
- `rich` - Console output
- `jupyter` - Notebook UI

### Internal Dependencies
```
main.py → core → tools
       → helpers

core → helpers
    → tools

tools → helpers (minimal)

helpers → (no internal deps)
```

## Testing Strategy

### Current State
- Manual testing via main.py and notebook
- No automated tests yet

### Future Testing
- Unit tests for helpers/
- Integration tests for core/
- Tool tests for tools/
- End-to-end tests for full execution

## Performance Considerations

### Bottlenecks
1. LLM API calls (slowest)
2. File I/O operations
3. Context loading (one-time cost)

### Optimizations
- Context loaded once per session
- Config cached globally
- Logs written asynchronously
- File operations sandboxed to output/

## Security Considerations

### Sandboxing
- All file operations restricted to `./output/`
- No system commands without validation
- Context includes safety rules

### Safety Rules
- Defined in `context/no-goes.md`
- Injected into agent backstory
- Agent must follow these rules

## Next Steps

**For understanding architecture**:
- [Architecture Overview](overview.md)
- [Context System](context-system.md)
- [Logging System](logging-system.md)

**For development**:
- [Adding Tools](../guides/adding-tools.md)
- [Creating Agents](../guides/creating-agents.md)
- [Modifying Code](../development/modifying-code.md)
