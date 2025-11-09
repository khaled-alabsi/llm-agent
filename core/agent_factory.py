"""
CrewAI Agent Factory
Creates and configures agents and crews
"""

from crewai import Agent, Task, Crew, Process
from typing import List, Optional
from .llm_config import setup_llm
from .context_loader import load_context_files, build_context_prompt, load_prompt_template
from tools.file_tools import (
    create_file_tool,
    read_file_tool,
    list_directory_tool,
    create_directory_tool,
)
from tools.code_tools import format_code_tool, validate_json_tool
from helpers.config_loader import get_config


def create_coder_agent(llm=None, verbose: bool = True) -> Agent:
    """
    Create a senior full-stack developer agent

    Args:
        llm: Language model instance (will create if None)
        verbose: Enable verbose output

    Returns:
        Configured CrewAI Agent
    """
    if llm is None:
        llm = setup_llm()

    config = get_config()

    # Load context
    context = load_context_files()
    context_prompt = build_context_prompt(context)

    # Get agent configuration
    agent_config = config.get_section('agent')
    role = agent_config.get('role', 'Senior Full-Stack Developer')
    goal = agent_config.get('goal', 'Build high-quality web applications')
    backstory = agent_config.get('backstory', 'Experienced developer')

    # Enhance backstory with context
    enhanced_backstory = f"""{backstory}

{context_prompt}

You have access to the following tools:
- create_file_tool: Create new files with content
- read_file_tool: Read existing file content
- list_directory_tool: List files in a directory
- create_directory_tool: Create new directories
- format_code_tool: Format and validate code
- validate_json_tool: Validate JSON syntax

IMPORTANT INSTRUCTIONS:
1. Always work in the ./output directory
2. Follow ALL safety rules and no-goes
3. Adhere to coding standards
4. Create clean, well-documented code
5. Make the website responsive and accessible
6. Use modern React patterns and Tailwind CSS
7. Test your code mentally before creating files
8. Never hardcode sensitive data
9. Always include error handling
10. Make components reusable
"""

    # Create agent with tools
    agent = Agent(
        role=role,
        goal=goal,
        backstory=enhanced_backstory,
        llm=llm,
        tools=[
            create_file_tool,
            read_file_tool,
            list_directory_tool,
            create_directory_tool,
            format_code_tool,
            validate_json_tool,
        ],
        verbose=verbose,
        allow_delegation=False,
        max_iter=agent_config.get('max_iterations', 25),
    )

    return agent


def create_website_task(agent: Agent, prompt_override: Optional[str] = None) -> Task:
    """
    Create a task to build a personal website

    Args:
        agent: The agent to assign the task to
        prompt_override: Override the default prompt (optional)

    Returns:
        Configured Task
    """
    if prompt_override:
        description = prompt_override
    else:
        description = load_prompt_template('build-website')

    expected_output = """
A complete, functional personal website with:
- All files created in ./output directory
- Proper React component structure
- Tailwind CSS styling
- Responsive design
- Dark mode support
- Contact form
- Portfolio section
- README with setup instructions
- package.json with dependencies
- All files properly formatted and documented
"""

    task = Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )

    return task


def create_coder_crew(
    custom_prompt: Optional[str] = None,
    verbose: bool = True
) -> Crew:
    """
    Create a complete CrewAI crew for web development

    Args:
        custom_prompt: Custom task prompt (uses default if None)
        verbose: Enable verbose output

    Returns:
        Configured Crew ready to execute
    """
    # Setup LLM
    llm = setup_llm()

    # Create agent
    coder = create_coder_agent(llm=llm, verbose=verbose)

    # Create task
    task = create_website_task(coder, prompt_override=custom_prompt)

    # Create crew
    crew = Crew(
        agents=[coder],
        tasks=[task],
        process=Process.sequential,
        verbose=verbose,
    )

    return crew
