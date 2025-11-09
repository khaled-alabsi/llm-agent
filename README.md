# CrewAI Coder Agent

A sophisticated AI-powered coding agent using CrewAI and local LLMs (via LM Studio) to autonomously build complete web applications.

## Overview

This project demonstrates how to build production-grade AI agents using CrewAI framework with local LLMs. The agent can autonomously create complete web projects (like personal websites) with proper architecture, clean code, and best practices.

## What Makes This Special

### Modern Architecture
- **Modular Design**: Separate folders for core, tools, helpers, and context
- **Configuration-Driven**: YAML configuration for easy customization
- **Session Logging**: Comprehensive logging with one file per session
- **Context-Aware**: Loads skills, guidelines, and safety rules
- **Task-Based Documentation**: Complete docs with navigation by task

### CrewAI Integration
- Uses CrewAI framework for agent orchestration
- Connects to local LLM (LM Studio) instead of OpenAI
- Custom tools for file operations and code generation
- Structured task execution with proper output

### Learning-Focused
- Complete transparency with detailed logging
- Well-documented code
- Clear separation of concerns
- Extensible architecture
- **Documentation Entry Point**: [docs/index.md](docs/index.md) - Start here!

## 📚 Documentation

**Start Here**: [docs/index.md](docs/index.md)

The documentation is organized by **task**, not by component. Jump directly to what you need:

- **First time?** → [Quick Start Guide](docs/guides/quick-start.md)
- **Want to add tools?** → [Adding Tools Guide](docs/guides/adding-tools.md)
- **Understanding the code?** → [Code Structure](docs/architecture/code-structure.md)
- **See all options** → [Documentation Index](docs/index.md)

### Documentation Structure
```
docs/
├── index.md              # 👈 START HERE - Task-based navigation
├── architecture/         # System design
├── guides/              # How-to guides
├── api/                 # API reference
└── development/         # Development guides
```

### Project Requirements
See [PROJECT_REQUIREMENTS.md](PROJECT_REQUIREMENTS.md) for complete project specifications.

## Project Structure

```
llm-agent/
├── config.yaml                  # Main configuration file
├── main.py                      # CLI entry point
├── agent_control.ipynb          # Jupyter notebook UI
├── requirements.txt             # Python dependencies
│
├── core/                        # Core agent logic
│   ├── __init__.py
│   ├── llm_config.py           # LLM setup for LM Studio
│   ├── agent_factory.py        # Create agents and crews
│   └── context_loader.py       # Load context files
│
├── tools/                       # Custom CrewAI tools
│   ├── __init__.py
│   ├── file_tools.py           # File operations
│   └── code_tools.py           # Code validation
│
├── helpers/                     # Utility functions
│   ├── __init__.py
│   ├── logger.py               # Session-based logging
│   ├── config_loader.py        # YAML config loader
│   └── file_utils.py           # File utilities
│
├── context/                     # Agent knowledge base
│   ├── no-goes.md              # Safety rules
│   ├── guidelines/
│   │   └── coding-standards.md
│   ├── skills/
│   │   ├── react-development.md
│   │   └── web-development.md
│   └── examples/
│       └── personal-website-example.md
│
├── prompts/                     # Task prompts
│   └── build-website.md        # Website building task
│
├── logs/                        # Session logs (gitignored)
│   └── .gitkeep
│
└── output/                      # Generated projects (gitignored)
    └── .gitkeep
```

## Prerequisites

### 1. LM Studio Setup
- Download and install [LM Studio](https://lmstudio.ai/)
- Load the Qwen3-Coder-30B model (or any compatible model)
- Start the local server (default: http://localhost:1234)
- Ensure the server is running before executing the agent

### 2. Python Environment
- Python 3.10 or higher
- pip package manager

## Installation

### 1. Clone/Navigate to Repository
```bash
cd /path/to/llm-agent
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Command Line (Recommended for First Run)

```bash
python main.py
```

This will:
1. Load configuration from `config.yaml`
2. Initialize the agent with context
3. Create a personal website in `./output`
4. Save session logs to `./logs`

### Option 2: Jupyter Notebook (Interactive)

```bash
jupyter notebook agent_control.ipynb
```

The notebook provides:
- Interactive control over agent execution
- Custom prompt editing
- Real-time log viewing
- File inspection tools
- Session metrics

## Configuration

### Main Config (`config.yaml`)

#### LLM Settings
```yaml
llm:
  base_url: "http://localhost:1234/v1"
  model: "qwen/qwen3-coder-30b"
  temperature: 0.7
  max_tokens: 4000
```

#### Agent Settings
```yaml
agent:
  role: "Senior Full-Stack Developer"
  goal: "Build high-quality, modern web applications"
  max_iterations: 25
```

#### Logging Settings
```yaml
logging:
  directory: "./logs"
  level: "INFO"
  format: "detailed"
  log_tool_calls: true
  log_llm_responses: true
```

### Context Files

#### Safety Rules (`context/no-goes.md`)
- Absolute prohibitions (security vulnerabilities, bad practices)
- Warning zones
- Recommended patterns
- Emergency stop conditions

#### Coding Standards (`context/guidelines/coding-standards.md`)
- Naming conventions
- Code organization
- React/JavaScript standards
- Error handling
- Performance optimization

#### Skills (`context/skills/`)
- React development patterns
- Web development best practices
- Modern JavaScript techniques
- CSS/Tailwind expertise

### Custom Prompts

Edit `prompts/build-website.md` or create new ones to change what the agent builds.

## How It Works

### 1. Initialization
```python
# Load configuration
config = load_config()

# Setup LLM connection (LM Studio)
llm = setup_llm()

# Load context (skills, guidelines, safety rules)
context = load_context_files()
```

### 2. Agent Creation
```python
# Create agent with tools and context
agent = create_coder_agent(llm=llm)

# Agent has access to:
# - create_file_tool
# - read_file_tool
# - list_directory_tool
# - create_directory_tool
# - format_code_tool
# - validate_json_tool
```

### 3. Task Execution
```python
# Create task from prompt
task = create_website_task(agent)

# Create crew
crew = Crew(agents=[agent], tasks=[task])

# Execute
result = crew.kickoff()
```

### 4. Output
- Generated files in `./output/`
- Session logs in `./logs/`
- Metrics (LLM calls, tokens, duration, etc.)

## Logging System

### Session-Based Logging
Each execution creates:
- `logs/session_YYYYMMDD_HHMMSS.log` - Human-readable log
- `logs/session_YYYYMMDD_HHMMSS.json` - Structured data

### What's Logged
- Session start/end timestamps
- LLM API calls (request/response, tokens, duration)
- Tool executions (arguments, results, duration)
- Errors and warnings
- Session metrics

### Example Log Metrics
```json
{
  "metrics": {
    "total_llm_calls": 15,
    "total_tool_calls": 42,
    "total_tokens": 8543,
    "errors": 0
  }
}
```

## Output Structure

Generated projects follow this structure:
```
output/personal-website/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── Hero.jsx
│   │   ├── About.jsx
│   │   ├── Skills.jsx
│   │   ├── Portfolio.jsx
│   │   └── Contact.jsx
│   ├── data/
│   │   └── constants.js
│   ├── styles/
│   │   └── index.css
│   ├── App.jsx
│   └── main.jsx
├── package.json
├── tailwind.config.js
├── vite.config.js
└── README.md
```

## Customization

### Add New Tools

Create a new tool in `tools/`:

```python
from crewai.tools import tool

@tool("My Custom Tool")
def my_custom_tool(param: str) -> str:
    """
    Description of what the tool does

    Args:
        param: Parameter description

    Returns:
        Result description
    """
    # Tool logic here
    return result
```

Register in `core/agent_factory.py`:
```python
agent = Agent(
    tools=[
        # existing tools...
        my_custom_tool,
    ]
)
```

### Add New Context

1. Create markdown file in `context/skills/` or `context/guidelines/`
2. Load in `core/context_loader.py`
3. Include in `build_context_prompt()`

### Create New Task Prompts

1. Create markdown file in `prompts/`
2. Load with `load_prompt_template('your-prompt-name')`
3. Use in task creation

## Extending the Agent

### Multi-Agent Setup

```python
from crewai import Agent, Task, Crew, Process

# Create multiple specialized agents
designer = create_designer_agent()
developer = create_developer_agent()
tester = create_tester_agent()

# Create tasks for each
design_task = Task(description="...", agent=designer)
dev_task = Task(description="...", agent=developer)
test_task = Task(description="...", agent=tester)

# Create crew with sequential process
crew = Crew(
    agents=[designer, developer, tester],
    tasks=[design_task, dev_task, test_task],
    process=Process.sequential
)
```

### Different Project Types

Create new prompts for different projects:
- `prompts/build-api.md` - REST API project
- `prompts/build-dashboard.md` - Admin dashboard
- `prompts/build-blog.md` - Blog platform

## Troubleshooting

### LM Studio Connection Issues
```bash
# Check if LM Studio is running
curl http://localhost:1234/v1/models

# If connection fails:
# 1. Ensure LM Studio server is started
# 2. Check port in config.yaml matches LM Studio
# 3. Verify model is loaded in LM Studio
```

### Agent Not Using Tools
- Check tool definitions are clear
- Verify prompt explicitly requires tool usage
- Increase `max_iterations` in config
- Review logs to see what agent is attempting

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Out of Memory
- Reduce `max_tokens` in config
- Use a smaller model
- Limit context size

## Examples

### Example 1: Build Personal Website
```bash
python main.py
```

### Example 2: Custom Prompt in Notebook
```python
custom_prompt = """
Create a React dashboard with:
- Authentication
- Data visualization
- User management
"""

crew = create_coder_crew(custom_prompt=custom_prompt)
result = crew.kickoff()
```

### Example 3: Configure for Different Model
Edit `config.yaml`:
```yaml
llm:
  model: "codellama/CodeLlama-34b"
  max_tokens: 2000
```

## Best Practices

1. **Start Small**: Test with simple prompts first
2. **Review Logs**: Check session logs to understand agent behavior
3. **Iterate**: Refine context and prompts based on results
4. **Context Matters**: Good context files = better output
5. **Monitor Tokens**: Watch token usage in logs
6. **Backup Output**: Copy good results before re-running

## Future Enhancements

Potential additions:
- [ ] Web UI for agent control
- [ ] Multi-agent collaboration
- [ ] Code testing and validation
- [ ] Git integration
- [ ] Database tool integration
- [ ] API documentation generation
- [ ] Automated testing
- [ ] Performance profiling

## Contributing

Feel free to extend this project:
- Add new tools
- Create new prompts
- Improve context files
- Add new agent types
- Enhance logging

## License

MIT License - Free to use and modify

## Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [LM Studio](https://lmstudio.ai/)
- [LangChain Documentation](https://python.langchain.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)

## Acknowledgments

- CrewAI framework by Crew AI
- LM Studio for local LLM hosting
- Qwen for the Qwen3-Coder model
