"""
Load context files (skills, guidelines, examples)
Provides context to the agent for better performance
"""

from pathlib import Path
from typing import Dict, List
from helpers.file_utils import read_markdown_file


def load_context_files() -> Dict[str, str]:
    """
    Load all context files from the context directory

    Returns:
        Dictionary with context content:
        {
            'no_goes': 'content...',
            'coding_standards': 'content...',
            'react_skills': 'content...',
            'web_skills': 'content...',
            'examples': 'content...'
        }
    """
    context = {}

    # Load no-goes
    try:
        context['no_goes'] = read_markdown_file('context/no-goes.md')
    except FileNotFoundError:
        context['no_goes'] = ""

    # Load coding standards
    try:
        context['coding_standards'] = read_markdown_file(
            'context/guidelines/coding-standards.md'
        )
    except FileNotFoundError:
        context['coding_standards'] = ""

    # Load skills
    try:
        context['react_skills'] = read_markdown_file(
            'context/skills/react-development.md'
        )
    except FileNotFoundError:
        context['react_skills'] = ""

    try:
        context['web_skills'] = read_markdown_file(
            'context/skills/web-development.md'
        )
    except FileNotFoundError:
        context['web_skills'] = ""

    # Load examples
    try:
        context['examples'] = read_markdown_file(
            'context/examples/personal-website-example.md'
        )
    except FileNotFoundError:
        context['examples'] = ""

    return context


def build_context_prompt(context: Dict[str, str]) -> str:
    """
    Build a comprehensive context prompt from loaded context files

    Args:
        context: Dictionary of context content

    Returns:
        Formatted context prompt
    """
    prompt_parts = []

    if context.get('no_goes'):
        prompt_parts.append("# SAFETY RULES AND PROHIBITIONS")
        prompt_parts.append("You MUST follow these rules at all times:")
        prompt_parts.append(context['no_goes'])
        prompt_parts.append("\n")

    if context.get('coding_standards'):
        prompt_parts.append("# CODING STANDARDS")
        prompt_parts.append("Follow these coding standards:")
        prompt_parts.append(context['coding_standards'])
        prompt_parts.append("\n")

    if context.get('react_skills'):
        prompt_parts.append("# REACT DEVELOPMENT KNOWLEDGE")
        prompt_parts.append(context['react_skills'])
        prompt_parts.append("\n")

    if context.get('web_skills'):
        prompt_parts.append("# WEB DEVELOPMENT KNOWLEDGE")
        prompt_parts.append(context['web_skills'])
        prompt_parts.append("\n")

    if context.get('examples'):
        prompt_parts.append("# REFERENCE EXAMPLES")
        prompt_parts.append(context['examples'])
        prompt_parts.append("\n")

    return "\n".join(prompt_parts)


def load_prompt_template(prompt_name: str = "build-website") -> str:
    """
    Load a prompt template from the prompts directory

    Args:
        prompt_name: Name of the prompt file (without .md extension)

    Returns:
        Prompt content
    """
    try:
        return read_markdown_file(f'prompts/{prompt_name}.md')
    except FileNotFoundError:
        return f"Prompt template '{prompt_name}' not found"
