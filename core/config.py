"""Configuration helpers for the coder agent (YAML-backed)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml

DEFAULT_CONFIG_PATH = Path(__file__).with_suffix(".yaml")


@dataclass
class LLMConfig:
    base_url: str
    model: str
    temperature: float
    max_tokens: int
    log_dir: Optional[str | Path]

    @classmethod
    def load(cls, path: str | Path | None = None) -> "LLMConfig":
        config_path = Path(path) if path else DEFAULT_CONFIG_PATH
        data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        return cls(
            base_url=data.get("base_url", "http://localhost:1234/v1"),
            model=data.get("model", "qwen/qwen3-coder-30b"),
            temperature=float(data.get("temperature", 0.2)),
            max_tokens=int(data.get("max_tokens", 2000)),
            log_dir=data.get("log_dir", "logs"),
        )

    def prepare_log_dir(self) -> Optional[Path]:
        if self.log_dir is None:
            return None
        log_dir_path = Path(self.log_dir)
        log_dir_path.mkdir(parents=True, exist_ok=True)
        return log_dir_path
