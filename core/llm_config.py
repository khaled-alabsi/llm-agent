"""
LLM configuration for local models (LM Studio)
Configures LangChain to work with local LLM API
"""

from langchain_openai import ChatOpenAI
from helpers.config_loader import get_config


def setup_llm():
    """
    Setup and configure LLM for use with CrewAI

    Returns:
        Configured ChatOpenAI instance compatible with CrewAI

    The LLM is configured to connect to LM Studio's local API endpoint
    which provides an OpenAI-compatible interface.
    """
    config = get_config()

    # Get LLM configuration
    base_url = config.get('llm.base_url', 'http://localhost:1234/v1')
    model = config.get('llm.model', 'qwen/qwen3-coder-30b')
    temperature = config.get('llm.temperature', 0.7)
    max_tokens = config.get('llm.max_tokens', 4000)
    timeout = config.get('llm.timeout', 120)

    # Create ChatOpenAI instance
    # We use a dummy API key since LM Studio doesn't require one
    llm = ChatOpenAI(
        base_url=base_url,
        api_key="lm-studio",  # Dummy key for local LM Studio
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
    )

    return llm
