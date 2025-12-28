"""Configuration handling for the add-on."""

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Add-on configuration."""

    log_level: str = "info"

    @classmethod
    def from_options(cls, path: Path | None = None) -> "Config":
        """Load configuration from options.json.

        Args:
            path: Path to options.json (default: /data/options.json)

        Returns:
            Config instance with loaded options

        Raises:
            FileNotFoundError: If options.json doesn't exist
            json.JSONDecodeError: If options.json is invalid
        """
        if path is None:
            # Default path in Home Assistant add-on environment
            path = Path("/data/options.json")

            # Fallback for local development
            if not path.exists():
                path = Path("data/options.json")

            # If still doesn't exist, use defaults
            if not path.exists():
                logger.warning("Options file not found at %s, using defaults", path)
                return cls()

        logger.info("Loading configuration from %s", path)

        with open(path) as f:
            options = json.load(f)

        return cls(
            log_level=options.get("log_level", "info"),
        )

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables.

        Useful for local development without options.json.

        Returns:
            Config instance from environment variables
        """
        return cls(
            log_level=os.getenv("LOG_LEVEL", "info"),
        )
