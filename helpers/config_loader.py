"""
Configuration loader and manager
Loads config from YAML file and provides easy access
"""

import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigLoader:
    """Configuration loader and manager"""

    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize config loader

        Args:
            config_path: Path to YAML config file
        """
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.load()

    def load(self):
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation path

        Args:
            key_path: Dot-separated path to config value (e.g., 'llm.model')
            default: Default value if key not found

        Returns:
            Configuration value

        Example:
            config.get('llm.model') -> 'qwen/qwen3-coder-30b'
        """
        keys = key_path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section

        Args:
            section: Section name

        Returns:
            Section dictionary
        """
        return self.config.get(section, {})

    def reload(self):
        """Reload configuration from file"""
        self.load()

    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access"""
        return self.config[key]

    def __contains__(self, key: str) -> bool:
        """Check if key exists"""
        return key in self.config


# Global config instance
_config: Optional[ConfigLoader] = None


def load_config(config_path: str = "config.yaml") -> ConfigLoader:
    """
    Load configuration file

    Args:
        config_path: Path to config file

    Returns:
        ConfigLoader instance
    """
    global _config
    _config = ConfigLoader(config_path)
    return _config


def get_config() -> ConfigLoader:
    """
    Get global config instance

    Returns:
        ConfigLoader instance

    Raises:
        RuntimeError: If config not loaded yet
    """
    global _config
    if _config is None:
        _config = load_config()
    return _config
