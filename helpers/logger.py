"""Logging helper for the coder agent."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional


def get_logger(name: str = "coder_agent", log_dir: Optional[str | Path] = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_dir:
        log_dir_path = Path(log_dir)
        log_dir_path.mkdir(parents=True, exist_ok=True)
        # Delay file creation until the first write so empty log files
        # are not created when no messages are emitted.
        file_handler = logging.FileHandler(log_dir_path / f"{name}.log", delay=True)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
