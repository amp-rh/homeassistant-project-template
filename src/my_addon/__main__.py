"""Main entry point for the add-on."""

import asyncio
import logging
import sys

from my_addon.config import Config
from my_addon.server import start_server


def setup_logging(log_level: str = "info") -> None:
    """Setup logging configuration."""
    import colorlog

    log_level_map = {
        "trace": logging.DEBUG,
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "fatal": logging.CRITICAL,
    }

    level = log_level_map.get(log_level.lower(), logging.INFO)

    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-8s%(reset)s "
            "%(blue)s%(name)s%(reset)s %(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
    )

    logging.basicConfig(level=level, handlers=[handler])


def main() -> int:
    """Run the add-on."""
    try:
        # Load configuration
        config = Config.from_options()
        setup_logging(config.log_level)

        logger = logging.getLogger(__name__)
        logger.info("Starting My Python Add-on v%s", "0.1.0")
        logger.info("Log level: %s", config.log_level)

        # Run the server
        asyncio.run(start_server(config))
        return 0

    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Received interrupt, shutting down...")
        return 0
    except Exception as e:
        logging.getLogger(__name__).exception("Fatal error: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
