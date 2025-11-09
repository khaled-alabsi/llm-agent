# CrewAI Coder Agent - Documentation Index

Welcome to the CrewAI Coder Agent documentation! This is your **entry point** - read only what you need based on your task.

## 🎯 Quick Task Navigation

Choose your task below to jump directly to the relevant documentation:

### For First-Time Users
- **"I want to run the agent for the first time"** → [Quick Start Guide](guides/quick-start.md)
- **"I want to understand what this project does"** → [Project Overview](architecture/overview.md)
- **"I need to install and setup everything"** → [Installation Guide](guides/installation.md)

### For Developers
- **"I want to add a new tool"** → [Adding Tools Guide](guides/adding-tools.md)
- **"I want to create a new agent"** → [Creating Agents Guide](guides/creating-agents.md)
- **"I want to modify the prompt"** → [Prompt Engineering Guide](guides/prompt-engineering.md)
- **"I want to understand the architecture"** → [Architecture Overview](architecture/overview.md)
- **"I want to understand the code structure"** → [Code Structure](architecture/code-structure.md)

### For Agent/AI Reading This
- **"I need to modify existing code"** → [Code Modification Guide](development/modifying-code.md)
- **"I need to add a new feature"** → [Feature Development Guide](development/adding-features.md)
- **"I need to fix a bug"** → [Debugging Guide](development/debugging.md)
- **"I need to understand the API"** → [API Reference](api/reference.md)

### For Configuration
- **"I want to change LLM settings"** → [Configuration Guide](guides/configuration.md)
- **"I want to use a different model"** → [Model Configuration](guides/model-setup.md)
- **"I want to customize agent behavior"** → [Agent Customization](guides/agent-customization.md)

### For Understanding Context System
- **"What are context files?"** → [Context System](architecture/context-system.md)
- **"How do I modify safety rules?"** → [Safety Rules Guide](guides/safety-rules.md)
- **"How do I add new skills?"** → [Skills Guide](guides/skills-management.md)

### For Logging and Debugging
- **"How does logging work?"** → [Logging System](architecture/logging-system.md)
- **"Where are the logs?"** → [Log Files Guide](guides/log-files.md)
- **"How do I debug the agent?"** → [Debugging Guide](development/debugging.md)

## 📚 Documentation Structure

```
docs/
├── index.md (YOU ARE HERE)
│
├── architecture/          # System design and architecture
│   ├── overview.md       # High-level architecture
│   ├── code-structure.md # Code organization
│   ├── context-system.md # How context works
│   └── logging-system.md # Logging architecture
│
├── guides/               # How-to guides
│   ├── quick-start.md   # Get started in 5 minutes
│   ├── installation.md  # Detailed installation
│   ├── configuration.md # Configuration options
│   ├── adding-tools.md  # Create custom tools
│   ├── creating-agents.md # Create new agents
│   ├── prompt-engineering.md # Write effective prompts
│   └── ...
│
├── api/                 # API reference
│   ├── reference.md    # Complete API reference
│   ├── tools.md        # Tools API
│   ├── helpers.md      # Helper functions
│   └── core.md         # Core module API
│
└── development/         # Development guides
    ├── modifying-code.md
    ├── adding-features.md
    ├── debugging.md
    └── testing.md
```

## 🚦 Decision Tree: Which Doc Should I Read?

### Starting Point
```
Are you running this for the first time?
├─ YES → Read: guides/quick-start.md
└─ NO → Continue below

Do you want to USE the agent or DEVELOP it?
├─ USE → Read: guides/quick-start.md OR guides/configuration.md
└─ DEVELOP → Continue below

What do you want to develop?
├─ Add new tool → Read: guides/adding-tools.md + api/tools.md
├─ Add new agent → Read: guides/creating-agents.md + api/core.md
├─ Modify prompts → Read: guides/prompt-engineering.md
├─ Change context → Read: architecture/context-system.md + guides/skills-management.md
├─ Fix bug → Read: development/debugging.md
└─ Add feature → Read: development/adding-features.md + architecture/code-structure.md
```

## 📖 Reading Order Recommendations

### For Complete Beginners
1. [Project Overview](architecture/overview.md) - 5 min read
2. [Quick Start Guide](guides/quick-start.md) - 10 min read
3. [Configuration Guide](guides/configuration.md) - 5 min read
4. Start experimenting!

### For Developers Adding Features
1. [Architecture Overview](architecture/overview.md) - 10 min read
2. [Code Structure](architecture/code-structure.md) - 15 min read
3. Specific guide for your task (see navigation above)
4. [API Reference](api/reference.md) - as needed

### For AI Agents Working on This Code
1. [Code Structure](architecture/code-structure.md) - Understand organization
2. [Context System](architecture/context-system.md) - Understand how you use context
3. [Code Modification Guide](development/modifying-code.md) - Safe modification practices
4. Specific API docs for modules you're modifying

## 🔍 Searching for Specific Topics

### Tool Development
- [Adding Tools Guide](guides/adding-tools.md)
- [Tools API Reference](api/tools.md)

### Agent Development
- [Creating Agents Guide](guides/creating-agents.md)
- [Agent Customization](guides/agent-customization.md)
- [Core API Reference](api/core.md)

### Configuration
- [Configuration Guide](guides/configuration.md)
- [Model Setup](guides/model-setup.md)
- config.yaml reference

### Context & Knowledge
- [Context System](architecture/context-system.md)
- [Skills Management](guides/skills-management.md)
- [Safety Rules](guides/safety-rules.md)

### Logging & Debugging
- [Logging System](architecture/logging-system.md)
- [Log Files Guide](guides/log-files.md)
- [Debugging Guide](development/debugging.md)

## 💡 Tips for Efficient Documentation Use

### For Humans
- Use the task navigation above to jump directly to what you need
- Don't read everything - focus on your immediate task
- Bookmark frequently used pages
- Use search (Cmd/Ctrl+F) within documents

### For AI Agents
- Read index.md first (this file) to understand navigation
- Only load documentation files relevant to your current task
- Follow the decision tree to find the right doc
- Use the API reference for exact function signatures

## 🆘 Still Lost?

If you can't find what you need:
1. Check the [FAQ](guides/faq.md)
2. Look at [Common Issues](development/troubleshooting.md)
3. Review the [Project Requirements](../PROJECT_REQUIREMENTS.md)
4. Check the main [README.md](../README.md)

## 📝 Documentation Principles

This documentation follows these principles:
- **Task-oriented**: Organized by what you want to DO, not by system components
- **Minimal reading**: You should only need to read 1-2 docs for most tasks
- **Progressive disclosure**: Start simple, go deep only when needed
- **AI-friendly**: Structured for both human and AI consumption
- **Always up-to-date**: Docs are treated as first-class code

## 🔄 Last Updated

This documentation was created alongside the project. If you find outdated information, please update it!

---

**Ready to start?** Pick your task from the navigation above and jump to the relevant doc!
