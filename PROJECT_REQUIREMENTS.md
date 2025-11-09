# Project Requirements

Complete requirements document for the Coder Agent project.

## Project Overview

**Goal**: Create an educational and production-ready AI coding agent  with local LLMs to autonomously build complete web applications.


#### 6.1 Folder Structure
- **REQ-6.1.1**: `core/` - Agent logic, LLM config, context loading
- **REQ-6.1.2**: `tools/` - Custom tools
- **REQ-6.1.3**: `helpers/` - Utility modules (logger, config, file utils)
- **REQ-6.1.4**: `context/` - Agent knowledge base
- **REQ-6.1.5**: `prompts/` - Task definition templates
- **REQ-6.1.6**: `logs/` - Session logs (gitignored)
- **REQ-6.1.7**: `generated_projects/` - Generated projects (gitignored but tracked)
- **REQ-6.1.8**: `docs/` - Documentation


- **REQ-6.2.3**: `context_loader.py` - Load context files

#### 6.3 Tools Module
- **REQ-6.3.1**: `file_tools.py` - File CRUD operations
- **REQ-6.3.2**: `code_tools.py` - Code validation/formatting

#### 6.4 Helpers Module
- **REQ-6.4.1**: `logger.py` - Session-based logging
- **REQ-6.4.2**: `config_loader.py` - YAML configuration management
- **REQ-6.4.3**: `file_utils.py` - File system utilities

#### 6.5 Modern Design Principles
- **REQ-6.5.1**: Single Responsibility Principle
- **REQ-6.5.2**: Dependency Injection
- **REQ-6.5.3**: Factory Pattern for agent creation
- **REQ-6.5.4**: Singleton Pattern for config
- **REQ-6.5.5**: Decorator Pattern for tools
- **REQ-6.5.6**: Clear separation of concerns
- **REQ-6.5.7**: Easy extensibility
- **REQ-6.5.8**: Minimal coupling between modules

### 7. User Interfaces

#### 7.1 CLI Interface
- **REQ-7.1.1**: `main.py` as primary entry point
- **REQ-7.1.2**: Display configuration on start
- **REQ-7.1.3**: Show session ID and log location
- **REQ-7.1.4**: Display progress during execution
- **REQ-7.1.5**: Show final results and metrics
- **REQ-7.1.6**: Handle Ctrl+C gracefully
- **REQ-7.1.7**: Save logs on error or interrupt

#### 7.2 Jupyter Notebook Interface
- **REQ-7.2.1**: `agent_control.ipynb` as interactive UI
- **REQ-7.2.2**: Cell for configuration viewing
- **REQ-7.2.3**: Cell for default prompt execution
- **REQ-7.2.4**: Cell for custom prompt execution
- **REQ-7.2.5**: Cell for viewing generated files
- **REQ-7.2.6**: Cell for inspecting specific files
- **REQ-7.2.7**: Cell for viewing session logs
- **REQ-7.2.8**: Cell for viewing metrics
- **REQ-7.2.9**: Markdown cells with instructions
- **REQ-7.2.10**: Quick reference section

### 8. Prompt System

#### 8.1 Prompt Templates
- **REQ-8.1.1**: Store prompts in `prompts/` directory
- **REQ-8.1.2**: Use markdown format for prompts
- **REQ-8.1.3**: `build-website.md` as default prompt
- **REQ-8.1.4**: Load prompts dynamically
- **REQ-8.1.5**: Support custom prompt override


