"""Core modules for CrewAI Coder Agent"""

from .llm_config import setup_llm
from .agent_factory import create_coder_agent, create_coder_crew
from .context_loader import load_context_files

__all__ = [
    'setup_llm',
    'create_coder_agent',
    'create_coder_crew',
    'load_context_files',
]
