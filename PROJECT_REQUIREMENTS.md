# Project Requirements

Complete requirements document for the CrewAI Coder Agent project.

## Project Overview

**Goal**: Create an educational and production-ready AI coding agent system using CrewAI framework with local LLMs to autonomously build complete web applications.

**Purpose**:
- Learn how to create agents in different ways and frameworks
- Understand tool usage and LLM response handling
- Experiment with agent-based development
- Build a flexible, extensible agent architecture

## Core Requirements

### 1. Agent Framework

#### 1.1 CrewAI Integration
- **REQ-1.1.1**: Use CrewAI framework for agent orchestration
- **REQ-1.1.2**: Support custom tool creation and registration
- **REQ-1.1.3**: Enable agent customization (role, goal, backstory)
- **REQ-1.1.4**: Support task definition and execution
- **REQ-1.1.5**: Allow sequential and parallel task processing

#### 1.2 Local LLM Support
- **REQ-1.2.1**: Connect to LM Studio local API
- **REQ-1.2.2**: Support Qwen/qwen3-coder-30b model
- **REQ-1.2.3**: Use OpenAI-compatible API interface
- **REQ-1.2.4**: Allow model configuration via YAML
- **REQ-1.2.5**: Support temperature, max_tokens, timeout configuration

### 2. Tool System

#### 2.1 Core Tools
- **REQ-2.1.1**: Implement file creation tool
- **REQ-2.1.2**: Implement file reading tool
- **REQ-2.1.3**: Implement directory listing tool
- **REQ-2.1.4**: Implement directory creation tool
- **REQ-2.1.5**: Implement code validation tool
- **REQ-2.1.6**: Implement JSON validation tool

#### 2.2 Tool Architecture
- **REQ-2.2.1**: Tools must use CrewAI @tool decorator
- **REQ-2.2.2**: Tools must have clear docstrings
- **REQ-2.2.3**: Tools must return string results
- **REQ-2.2.4**: Tools must include error handling
- **REQ-2.2.5**: Tools must be easily extensible

#### 2.3 Tool Response Format
- **REQ-2.3.1**: Success responses start with ✓
- **REQ-2.3.2**: Error responses start with ✗
- **REQ-2.3.3**: Warning responses start with ⚠
- **REQ-2.3.4**: Include descriptive messages in all responses

### 3. Logging System

#### 3.1 Session-Based Logging
- **REQ-3.1.1**: One log file per session
- **REQ-3.1.2**: Unique session ID per execution
- **REQ-3.1.3**: Session format: `session_YYYYMMDD_HHMMSS`
- **REQ-3.1.4**: Log files in `./logs/` directory
- **REQ-3.1.5**: Maximum 50 session files (configurable)

#### 3.2 Log Format
- **REQ-3.2.1**: Provide both .log (human-readable) and .json (structured) formats
- **REQ-3.2.2**: Include timestamps for all events
- **REQ-3.2.3**: Log LLM calls with full request/response
- **REQ-3.2.4**: Log tool calls with arguments and results
- **REQ-3.2.5**: Log errors with stack traces

#### 3.3 Log Content
- **REQ-3.3.1**: Log session start/end times
- **REQ-3.3.2**: Track total LLM calls
- **REQ-3.3.3**: Track total tool calls
- **REQ-3.3.4**: Track total tokens used
- **REQ-3.3.5**: Track errors count
- **REQ-3.3.6**: Calculate session duration

#### 3.4 LLM Response Visibility
- **REQ-3.4.1**: Show complete request payload including all tool schemas
- **REQ-3.4.2**: Show complete raw LLM response
- **REQ-3.4.3**: Show tool_calls array in response
- **REQ-3.4.4**: Save request/response to separate JSON files
- **REQ-3.4.5**: Display in console and save to files

### 4. Configuration System

#### 4.1 YAML Configuration
- **REQ-4.1.1**: Use config.yaml as central configuration
- **REQ-4.1.2**: Support dot-notation access (e.g., 'llm.model')
- **REQ-4.1.3**: Provide default values for all settings
- **REQ-4.1.4**: Allow runtime configuration reload
- **REQ-4.1.5**: Global config instance (singleton pattern)

#### 4.2 Configuration Sections
- **REQ-4.2.1**: LLM settings (provider, base_url, model, temperature, max_tokens)
- **REQ-4.2.2**: Agent settings (role, goal, backstory, max_iterations)
- **REQ-4.2.3**: Tools configuration (enabled tools, file extensions)
- **REQ-4.2.4**: Output configuration (directory, structure)
- **REQ-4.2.5**: Logging configuration (directory, level, format)
- **REQ-4.2.6**: Context configuration (directories for skills, guidelines, examples)
- **REQ-4.2.7**: Safety configuration (no-goes file, validation settings)

### 5. Context System

#### 5.1 Context Files
- **REQ-5.1.1**: Safety rules (no-goes.md) with absolute prohibitions
- **REQ-5.1.2**: Coding standards (coding-standards.md) with best practices
- **REQ-5.1.3**: React development skills (react-development.md)
- **REQ-5.1.4**: Web development skills (web-development.md)
- **REQ-5.1.5**: Example projects (personal-website-example.md)

#### 5.2 Context Structure
- **REQ-5.2.1**: `context/no-goes.md` - Safety rules
- **REQ-5.2.2**: `context/guidelines/` - Coding standards
- **REQ-5.2.3**: `context/skills/` - Technical knowledge
- **REQ-5.2.4**: `context/examples/` - Reference examples
- **REQ-5.2.5**: All context loaded on agent initialization

#### 5.3 Context Injection
- **REQ-5.3.1**: Inject context into agent backstory
- **REQ-5.3.2**: Build comprehensive context prompt
- **REQ-5.3.3**: Load context files from markdown
- **REQ-5.3.4**: Make context easily extensible

### 6. Code Architecture

#### 6.1 Folder Structure
- **REQ-6.1.1**: `core/` - Agent logic, LLM config, context loading
- **REQ-6.1.2**: `tools/` - Custom CrewAI tools
- **REQ-6.1.3**: `helpers/` - Utility modules (logger, config, file utils)
- **REQ-6.1.4**: `context/` - Agent knowledge base
- **REQ-6.1.5**: `prompts/` - Task definition templates
- **REQ-6.1.6**: `logs/` - Session logs (gitignored)
- **REQ-6.1.7**: `output/` - Generated projects (gitignored but tracked)
- **REQ-6.1.8**: `docs/` - Documentation

#### 6.2 Core Module
- **REQ-6.2.1**: `llm_config.py` - LLM setup for LM Studio
- **REQ-6.2.2**: `agent_factory.py` - Agent/crew creation
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

#### 8.2 Website Building Prompt
- **REQ-8.2.1**: Specify React + Tailwind CSS stack
- **REQ-8.2.2**: Define all required sections (Hero, About, Skills, Portfolio, Contact)
- **REQ-8.2.3**: Specify design requirements (responsive, dark mode, accessibility)
- **REQ-8.2.4**: Define code quality requirements
- **REQ-8.2.5**: Specify deliverables (file structure, documentation)
- **REQ-8.2.6**: Include success criteria checklist

### 9. Output Management

#### 9.1 Output Directory
- **REQ-9.1.1**: All generated files go to `./output/`
- **REQ-9.1.2**: Output directory is gitignored
- **REQ-9.1.3**: Keep directory structure with .gitkeep
- **REQ-9.1.4**: Support nested directory creation
- **REQ-9.1.5**: Prevent operations outside output directory

#### 9.2 File Structure
- **REQ-9.2.1**: Create proper React project structure
- **REQ-9.2.2**: Include package.json
- **REQ-9.2.3**: Include README.md
- **REQ-9.2.4**: Include configuration files (vite.config.js, tailwind.config.js)
- **REQ-9.2.5**: Organize code into components/

#### 9.3 Change Tracking
- **REQ-9.3.1**: Track output directory in git
- **REQ-9.3.2**: Ignore contents but keep structure
- **REQ-9.3.3**: Use .gitkeep for empty directories

### 10. Documentation

#### 10.1 Documentation Structure
- **REQ-10.1.1**: `docs/` folder with organized documentation
- **REQ-10.1.2**: `docs/index.md` as entry point
- **REQ-10.1.3**: Task-based navigation
- **REQ-10.1.4**: `docs/architecture/` - System design
- **REQ-10.1.5**: `docs/guides/` - How-to guides
- **REQ-10.1.6**: `docs/api/` - API reference
- **REQ-10.1.7**: `docs/development/` - Development guides

#### 10.2 Documentation Principles
- **REQ-10.2.1**: Task-oriented organization
- **REQ-10.2.2**: Minimal reading requirement
- **REQ-10.2.3**: Progressive disclosure
- **REQ-10.2.4**: AI-friendly structure
- **REQ-10.2.5**: Decision trees for navigation
- **REQ-10.2.6**: Clear "what to read next" sections

#### 10.3 Key Documentation Files
- **REQ-10.3.1**: `docs/index.md` - Main entry point with task navigation
- **REQ-10.3.2**: `docs/guides/quick-start.md` - 5-minute start guide
- **REQ-10.3.3**: `docs/architecture/code-structure.md` - Complete code structure
- **REQ-10.3.4**: `docs/guides/adding-tools.md` - Tool development guide
- **REQ-10.3.5**: `docs/guides/configuration.md` - Configuration reference
- **REQ-10.3.6**: `PROJECT_REQUIREMENTS.md` - This document

#### 10.4 Documentation for Agents
- **REQ-10.4.1**: Structured for LLM consumption
- **REQ-10.4.2**: Clear task-to-doc mapping
- **REQ-10.4.3**: Minimal context needed
- **REQ-10.4.4**: Code examples in every guide
- **REQ-10.4.5**: API signatures with types

### 11. Dependencies

#### 11.1 Core Dependencies
- **REQ-11.1.1**: crewai>=0.41.0
- **REQ-11.1.2**: crewai-tools>=0.8.0
- **REQ-11.1.3**: langchain>=0.1.0
- **REQ-11.1.4**: langchain-community>=0.0.20
- **REQ-11.1.5**: langchain-openai>=0.0.5

#### 11.2 Utility Dependencies
- **REQ-11.2.1**: pydantic>=2.5.0
- **REQ-11.2.2**: pyyaml>=6.0
- **REQ-11.2.3**: python-dotenv>=1.0.0
- **REQ-11.2.4**: requests>=2.31.0

#### 11.3 UI Dependencies
- **REQ-11.3.1**: jupyter>=1.0.0
- **REQ-11.3.2**: ipython>=8.12.0

#### 11.4 Display Dependencies
- **REQ-11.4.1**: colorama>=0.4.6
- **REQ-11.4.2**: rich>=13.7.0

### 12. Safety and Security

#### 12.1 No-Goes (Absolute Prohibitions)
- **REQ-12.1.1**: No hardcoded credentials
- **REQ-12.1.2**: No SQL injection vulnerabilities
- **REQ-12.1.3**: No XSS vulnerabilities
- **REQ-12.1.4**: No insecure dependencies
- **REQ-12.1.5**: No exposed sensitive data
- **REQ-12.1.6**: No code without error handling
- **REQ-12.1.7**: No overwriting without confirmation
- **REQ-12.1.8**: No operations outside project directory
- **REQ-12.1.9**: No system commands without safeguards
- **REQ-12.1.10**: No generating SVG/PNG (use placeholders)

#### 12.2 Code Quality Requirements
- **REQ-12.2.1**: All functions must have docstrings
- **REQ-12.2.2**: Use type hints throughout
- **REQ-12.2.3**: Follow PEP 8 style guide
- **REQ-12.2.4**: No magic numbers (use constants)
- **REQ-12.2.5**: DRY principle (no duplicate code)
- **REQ-12.2.6**: Proper error handling everywhere

#### 12.3 Sandboxing
- **REQ-12.3.1**: All file operations limited to ./output/
- **REQ-12.3.2**: Validate paths before operations
- **REQ-12.3.3**: No access to parent directories
- **REQ-12.3.4**: No system-wide changes

### 13. Generated Code Requirements

#### 13.1 Web Application Stack
- **REQ-13.1.1**: React 18+ with functional components
- **REQ-13.1.2**: Tailwind CSS for styling
- **REQ-13.1.3**: Vite as build tool
- **REQ-13.1.4**: Modern ES6+ JavaScript
- **REQ-13.1.5**: TypeScript support (optional)

#### 13.2 Application Features
- **REQ-13.2.1**: Responsive design (mobile-first)
- **REQ-13.2.2**: Dark mode support
- **REQ-13.2.3**: Smooth animations
- **REQ-13.2.4**: Contact form with validation
- **REQ-13.2.5**: Portfolio/project showcase
- **REQ-13.2.6**: Skills section
- **REQ-13.2.7**: About section
- **REQ-13.2.8**: Navigation with smooth scrolling

#### 13.3 Code Quality for Generated Code
- **REQ-13.3.1**: Well-documented components
- **REQ-13.3.2**: Reusable component structure
- **REQ-13.3.3**: Proper file organization
- **REQ-13.3.4**: No hardcoded data (use constants)
- **REQ-13.3.5**: Accessibility compliance
- **REQ-13.3.6**: PropTypes or TypeScript types

#### 13.4 Documentation for Generated Code
- **REQ-13.4.1**: README with setup instructions
- **REQ-13.4.2**: README with available scripts
- **REQ-13.4.3**: README with customization guide
- **REQ-13.4.4**: Comments in complex code
- **REQ-13.4.5**: Package.json with all dependencies

### 14. Educational Requirements

#### 14.1 Learning Transparency
- **REQ-14.1.1**: Show complete LLM request/response
- **REQ-14.1.2**: Show tool execution details
- **REQ-14.1.3**: Explain what agent is doing
- **REQ-14.1.4**: Display token usage
- **REQ-14.1.5**: Show execution duration

#### 14.2 Code Understanding
- **REQ-14.2.1**: Clear code comments
- **REQ-14.2.2**: Comprehensive docstrings
- **REQ-14.2.3**: Architecture documentation
- **REQ-14.2.4**: Design pattern explanations
- **REQ-14.2.5**: Example usage code

#### 14.3 Extensibility
- **REQ-14.3.1**: Easy to add new tools
- **REQ-14.3.2**: Easy to add new agents
- **REQ-14.3.3**: Easy to customize prompts
- **REQ-14.3.4**: Easy to modify context
- **REQ-14.3.5**: Well-documented extension points

### 15. Performance Requirements

#### 15.1 Execution
- **REQ-15.1.1**: Complete task in reasonable time (3-10 minutes)
- **REQ-15.1.2**: Handle LLM timeouts gracefully
- **REQ-15.1.3**: Efficient context loading (once per session)
- **REQ-15.1.4**: Minimal unnecessary file operations

#### 15.2 Logging
- **REQ-15.2.1**: Asynchronous log writing
- **REQ-15.2.2**: Efficient JSON serialization
- **REQ-15.2.3**: Automatic log file rotation
- **REQ-15.2.4**: Maximum log file size limit

### 16. Git and Version Control

#### 16.1 Gitignore
- **REQ-16.1.1**: Ignore Python cache (__pycache__, *.pyc)
- **REQ-16.1.2**: Ignore virtual environment (.venv/)
- **REQ-16.1.3**: Ignore log files (logs/*.log, logs/*.json)
- **REQ-16.1.4**: Ignore output contents (output/*)
- **REQ-16.1.5**: Ignore IDE files (.vscode/, .idea/)
- **REQ-16.1.6**: Ignore OS files (.DS_Store, Thumbs.db)
- **REQ-16.1.7**: Keep directory structure (.gitkeep files)

#### 16.2 Repository Structure
- **REQ-16.2.1**: Track all source code
- **REQ-16.2.2**: Track documentation
- **REQ-16.2.3**: Track configuration files
- **REQ-16.2.4**: Track context files
- **REQ-16.2.5**: Track prompt templates
- **REQ-16.2.6**: Track directory structure with .gitkeep

### 17. Error Handling

#### 17.1 LLM Errors
- **REQ-17.1.1**: Handle connection errors
- **REQ-17.1.2**: Handle timeout errors
- **REQ-17.1.3**: Handle invalid responses
- **REQ-17.1.4**: Retry logic for transient errors
- **REQ-17.1.5**: Clear error messages

#### 17.2 Tool Errors
- **REQ-17.2.1**: Validate all inputs
- **REQ-17.2.2**: Handle file not found
- **REQ-17.2.3**: Handle permission errors
- **REQ-17.2.4**: Handle disk space errors
- **REQ-17.2.5**: Return descriptive error messages

#### 17.3 Configuration Errors
- **REQ-17.3.1**: Validate config file on load
- **REQ-17.3.2**: Provide default values
- **REQ-17.3.3**: Clear error for missing config
- **REQ-17.3.4**: Clear error for invalid values

### 18. Testing Requirements

#### 18.1 Manual Testing
- **REQ-18.1.1**: Test via main.py execution
- **REQ-18.1.2**: Test via notebook execution
- **REQ-18.1.3**: Verify generated code works
- **REQ-18.1.4**: Check log files completeness
- **REQ-18.1.5**: Validate output structure

#### 18.2 Future Automated Testing
- **REQ-18.2.1**: Unit tests for helpers/
- **REQ-18.2.2**: Integration tests for core/
- **REQ-18.2.3**: Tool execution tests
- **REQ-18.2.4**: End-to-end tests

## Implementation Status

### Completed ✅
- [x] CrewAI integration
- [x] Local LLM support (LM Studio)
- [x] All core tools implemented
- [x] Session-based logging
- [x] Complete request/response logging
- [x] YAML configuration system
- [x] Context system (skills, guidelines, no-goes, examples)
- [x] Modern code architecture (core, tools, helpers)
- [x] CLI interface (main.py)
- [x] Jupyter notebook UI
- [x] Prompt system with templates
- [x] Output directory management
- [x] Documentation with task-based navigation
- [x] Safety rules and validation
- [x] Gitignore and version control setup
- [x] Error handling throughout
- [x] Project requirements documentation

### Future Enhancements 🔮
- [ ] Automated testing suite
- [ ] Multi-agent collaboration
- [ ] Web UI interface
- [ ] Code testing/validation tools
- [ ] Database integration tools
- [ ] API integration examples
- [ ] Performance profiling
- [ ] Advanced monitoring dashboard

## Success Criteria

The project is considered successful if:
1. Agent can build complete, functional web applications
2. All logs show complete transparency (full LLM request/response)
3. Tools work reliably with proper error handling
4. Configuration is flexible and well-documented
5. Code follows modern design principles
6. Documentation enables quick task completion
7. Both interfaces (CLI and notebook) work seamlessly
8. Generated code follows best practices
9. Safety rules are enforced
10. Educational value is high (easy to learn from)

## Maintenance Requirements

### Documentation
- Keep docs in sync with code changes
- Update examples when APIs change
- Add new guides for new features

### Dependencies
- Review and update dependencies quarterly
- Test with new CrewAI versions
- Ensure LM Studio compatibility

### Context Files
- Update skills as technologies evolve
- Add new examples as patterns emerge
- Refine safety rules based on issues

## Version History

- **v1.0.0** (2025-11-09): Initial implementation with all core requirements
  - CrewAI integration
  - Complete logging system
  - Context-aware agent
  - Documentation system
  - CLI and notebook interfaces

## References

- CrewAI Documentation: https://docs.crewai.com/
- LM Studio: https://lmstudio.ai/
- LangChain Documentation: https://python.langchain.com/
- Project README: [README.md](README.md)
- Documentation Index: [docs/index.md](docs/index.md)
