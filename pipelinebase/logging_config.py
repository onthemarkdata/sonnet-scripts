import logging
import os
import sys


def setup_logging(name=None, level=None):
    """
    Configure and return a logger instance.

    Args:
        name: Logger name (defaults to root logger if None)
        level: Log level (defaults to INFO, can be overridden by LOG_LEVEL env var)

    Returns:
        Configured logger instance
    """
    if level is None:
        level_name = os.getenv("LOG_LEVEL", "INFO").upper()
        level = getattr(logging, level_name, logging.INFO)

    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(level)
    return logger
