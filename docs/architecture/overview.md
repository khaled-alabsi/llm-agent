# Architecture Overview

High-level architecture of the CrewAI Coder Agent system.

## System Design

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                                                              │
│    main.py (CLI)          agent_control.ipynb (Notebook)   │
└──────────────────┬───────────────────────┬─────────────────┘
                   │                       │
                   v                       v
┌─────────────────────────────────────────────────────────────┐
│                      Core Layer                              │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  LLM Config  │  │Agent Factory │  │Context Loader│     │
│  │              │  │              │  │              │     │
│  │ - Setup LLM  │  │ - Create     │  │ - Load       │     │
│  │ - Configure  │  │   Agent      │  │   Skills     │     │
│  │   OpenAI     │  │ - Create     │  │ - Load       │     │
│  │   Client     │  │   Tasks      │  │   Guidelines │     │
│  │              │  │ - Create     │  │ - Build      │     │
│  │              │  │   Crew       │  │   Context    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────────────┬──────────────────────┬─────────────────┘
                   │                      │
                   v                      v
┌─────────────────────────────────────────────────────────────┐
│                    CrewAI Framework                          │
│                                                              │
│         Agent → Task → Tools → LLM → Response               │
└──────────────────┬──────────────────────┬─────────────────┘
                   │                      │
    ┌──────────────┴──────────┐         ┌┴───────────────┐
    v                         v         v                v
┌──────────┐           ┌─────────────────────┐    ┌──────────┐
│  Tools   │           │   Helper Modules    │    │  Config  │
│          │           │                     │    │          │
│ - File   │           │  ┌────────┐         │    │ - YAML   │
│   Ops    │           │  │ Logger │         │    │   Loader │
│ - Code   │           │  │        │         │    │ - Get    │
│   Tools  │           │  └────────┘         │    │   Values │
│          │           │  ┌────────┐         │    │          │
│          │           │  │ Config │         │    │          │
│          │           │  │        │         │    │          │
│          │           │  └────────┘         │    │          │
│          │           │  ┌────────┐         │    │          │
│          │           │  │  File  │         │    │          │
│          │           │  │  Utils │         │    │          │
│          │           │  └────────┘         │    │          │
└──────────┘           └─────────────────────┘    └──────────┘
```

## Data Flow

### 1. Initialization Phase

```
User runs main.py
    ↓
Load config.yaml
    ↓
Create SessionLogger
    ↓
Setup LLM (connect to LM Studio)
    ↓
Load Context Files
    ├── no-goes.md
    ├── coding-standards.md
    ├── react-development.md
    ├── web-development.md
    └── examples.md
    ↓
Create Agent with:
    ├── Role & Goal
    ├── Context-enhanced Backstory
    └── Registered Tools
    ↓
Load Task Prompt
    ↓
Create Crew
```

### 2. Execution Phase

```
crew.kickoff()
    ↓
Agent receives task
    ↓
┌─────────────────────────────────────┐
│  Agent Decision Loop                │
│  (Iterates until task complete)     │
│                                     │
│  1. Analyze task requirements      │
│     ↓                               │
│  2. Decide: Use tool or respond?   │
│     ↓                               │
│  3a. If tool needed:               │
│      - Call LLM with tools list    │
│      - LLM responds with tool_call │
│      - Execute tool                │
│      - Log tool execution          │
│      - Send result to LLM          │
│      - Go to step 1                │
│     ↓                               │
│  3b. If no tool needed:            │
│      - Generate final response     │
│      - Return result               │
│      - Exit loop                   │
└─────────────────────────────────────┘
    ↓
Save session logs
    ↓
Display results
```

### 3. Tool Execution Flow

```
LLM decides to use tool
    ↓
Returns tool_call JSON:
{
  "id": "call_123",
  "function": {
    "name": "create_file",
    "arguments": "{\"path\": \"...\", \"content\": \"...\"}"
  }
}
    ↓
Agent parses tool_call
    ↓
Find tool by name
    ↓
Parse arguments from JSON string
    ↓
Execute tool function
    ↓
Log execution
    ├── Tool name
    ├── Arguments
    ├── Result
    └── Duration
    ↓
Return result to LLM
    ↓
LLM continues with result
```

## Key Components

### 1. Core Module

**Purpose**: Agent orchestration and LLM integration

**Files**:
- `llm_config.py` - LLM setup
- `agent_factory.py` - Agent creation
- `context_loader.py` - Context management

**Responsibilities**:
- Configure LLM connection
- Create and configure agents
- Load knowledge base (context)
- Build comprehensive prompts

### 2. Tools Module

**Purpose**: Provide capabilities to the agent

**Files**:
- `file_tools.py` - File operations
- `code_tools.py` - Code validation

**Responsibilities**:
- Execute file CRUD operations
- Validate code and JSON
- Return success/error messages
- Log all operations

### 3. Helpers Module

**Purpose**: Utility functions and services

**Files**:
- `logger.py` - Session logging
- `config_loader.py` - Configuration
- `file_utils.py` - File utilities

**Responsibilities**:
- Manage session logs
- Load and provide config values
- File system operations
- Markdown file reading

### 4. Context System

**Purpose**: Provide knowledge to the agent

**Structure**:
```
context/
├── no-goes.md              # Safety rules
├── guidelines/
│   └── coding-standards.md # Best practices
├── skills/
│   ├── react-development.md
│   └── web-development.md
└── examples/
    └── personal-website-example.md
```

**Loaded Into**: Agent's backstory as comprehensive knowledge

## Design Patterns

### Factory Pattern
**Where**: `core/agent_factory.py`

Creates agents with all necessary configuration:
```python
def create_coder_agent() -> Agent:
    # Load context
    # Setup LLM
    # Configure agent
    # Register tools
    return configured_agent
```

### Singleton Pattern
**Where**: `helpers/config_loader.py`

Single global config instance:
```python
_config = None

def get_config() -> ConfigLoader:
    global _config
    if _config is None:
        _config = load_config()
    return _config
```

### Decorator Pattern
**Where**: All tool definitions

CrewAI's @tool decorator:
```python
@tool("Tool Name")
def my_tool(param: type) -> str:
    return result
```

### Session Pattern
**Where**: `helpers/logger.py`

One log file per session:
```python
class SessionLogger:
    def __init__(self, session_id):
        self.session_id = session_id
        self.events = []

    def log_event(self, ...):
        # Append to same session file
```

## Technology Stack

### Frameworks
- **CrewAI**: Agent orchestration framework
- **LangChain**: LLM abstraction layer
- **OpenAI API**: LLM communication protocol

### Infrastructure
- **LM Studio**: Local LLM server
- **Qwen3-Coder-30B**: Code generation model

### Python Libraries
- **pydantic**: Data validation
- **pyyaml**: Configuration files
- **rich**: Console formatting
- **jupyter**: Notebook interface

## Configuration Architecture

### Centralized Configuration
All settings in `config.yaml`:

```yaml
llm:          # LLM settings
agent:        # Agent behavior
tools:        # Tool configuration
output:       # Output management
logging:      # Log settings
context:      # Knowledge base paths
safety:       # Security settings
```

### Access Pattern
```python
from helpers import get_config

config = get_config()
model = config.get('llm.model')
```

## Logging Architecture

### Session-Based Logs
Each execution creates:
- `session_YYYYMMDD_HHMMSS.log` - Human readable
- `session_YYYYMMDD_HHMMSS.json` - Machine readable

### Log Levels
1. **Events**: Agent actions, decisions
2. **LLM Calls**: Full request/response
3. **Tool Calls**: Execution details
4. **Errors**: With context and stack traces

### Metrics Tracked
- Total LLM calls
- Total tool calls
- Total tokens used
- Errors count
- Execution duration

## Security Architecture

### Sandboxing
- All file operations limited to `./output/`
- Path validation before operations
- No parent directory access

### Safety Rules
Loaded from `context/no-goes.md`:
- Absolute prohibitions
- Code quality rules
- Security requirements

### Validation
- Input validation on all tools
- Config validation on load
- Path sanitization

## Scalability Considerations

### Current Design
- Single agent execution
- Sequential task processing
- Local LLM (limited by hardware)

### Future Scalability
- Multi-agent collaboration
- Parallel task execution
- Remote LLM support
- Distributed logging

## Extension Points

### Add New Tools
1. Create function in `tools/`
2. Decorate with `@tool()`
3. Register in agent factory

### Add New Agents
1. Define in `agent_factory.py`
2. Configure role/goal/backstory
3. Assign tools
4. Add to crew

### Add New Context
1. Create `.md` in `context/`
2. Load in `context_loader.py`
3. Include in context prompt

### Add New Prompts
1. Create `.md` in `prompts/`
2. Load with `load_prompt_template()`
3. Pass to task creation

## Next Steps

For detailed information:
- [Code Structure](code-structure.md) - Detailed code organization
- [Context System](context-system.md) - How context works
- [Logging System](logging-system.md) - Logging details
