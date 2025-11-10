"""LLM client abstraction for chat completions with tool-calling.

This module isolates HTTP details so the agent can switch providers
or endpoints (local OpenAI-compatible servers, or remote OpenAI) by
changing YAML config only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests

from core.config import LLMConfig


@dataclass
class ChatResult:
    raw: Dict[str, Any]


class LLMClient:
    """Simple chat client for OpenAI-compatible /chat/completions APIs."""

    def __init__(self, config: LLMConfig) -> None:
        self.config = config

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if (self.config.api_key or "").strip():
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    def chat(
        self,
        messages: List[Dict[str, Any]],
        *,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[str] = "auto",
        temperature: float = 0.2,
        max_tokens: int = 2000,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if tools:
            payload["tools"] = tools
            if tool_choice is not None:
                payload["tool_choice"] = tool_choice

        response = requests.post(
            f"{self.config.base_url.rstrip('/')}/chat/completions",
            json=payload,
            headers=self._headers(),
            timeout=120,
        )
        response.raise_for_status()
        return response.json()

