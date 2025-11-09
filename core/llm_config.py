"""
LLM configuration helpers.
Creates CrewAI-compatible LLM instances backed by LiteLLM.
"""

import os
from typing import Dict, Optional

from crewai import LLM

from helpers.config_loader import get_config


def _resolve_custom_provider(provider: Optional[str]) -> Optional[str]:
    """
    Convert user-friendly provider names into LiteLLM provider identifiers.

    Args:
        provider: Value from config.yaml (e.g., "lm_studio", "openai")

    Returns:
        Provider string understood by LiteLLM or None if not required.
    """
    if not provider:
        return None

    normalized = provider.lower()

    # Providers that CrewAI already supports natively should skip LiteLLM overrides
    if normalized in {"openai", "anthropic", "azure", "gemini", "bedrock"}:
        return None

    provider_mapping: Dict[str, str] = {
        "lm_studio": "openai",  # LM Studio exposes an OpenAI-compatible API
        "lmstudio": "openai",
        "ollama": "ollama",
        "groq": "groq",
        "huggingface": "huggingface",
        "together": "together_ai",
        "together_ai": "together_ai",
    }
    return provider_mapping.get(normalized, normalized)


def setup_llm():
    """
    Setup and configure LLM parameters for CrewAI.

    Returns:
        Configured CrewAI LLM instance.
    """
    config = get_config()

    base_url = config.get('llm.base_url')
    model = config.get('llm.model', 'qwen/qwen3-coder-30b')
    temperature = config.get('llm.temperature', 0.7)
    max_tokens = config.get('llm.max_tokens', 4000)
    timeout = config.get('llm.timeout', 120)
    provider = config.get('llm.provider', 'lm_studio')

    # Resolve API key with sensible fallbacks (LM Studio accepts any non-empty string)
    api_key = (
        config.get('llm.api_key')
        or os.getenv('LLM_API_KEY')
        or os.getenv('OPENAI_API_KEY')
        or ("lm-studio" if provider and provider.lower() in {"lm_studio", "lmstudio"} else None)
    )

    llm_params = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "timeout": timeout,
    }

    if api_key:
        llm_params["api_key"] = api_key

    if base_url:
        llm_params["base_url"] = base_url
        # CrewAI/LiteLLM expect api_base for some providers; mirror base_url when present.
        llm_params["api_base"] = base_url

    custom_provider = _resolve_custom_provider(provider)
    if custom_provider:
        llm_params["custom_llm_provider"] = custom_provider

    return LLM(**llm_params)
