"""
TTS Logger Utilities

Centralized logging configuration for TTS SDK operations.
Provides consistent logging across all TTS modules with configurable levels.
"""

import logging
from typing import Optional


def get_logger(
    name: str, level: Optional[int] = None, format_string: Optional[str] = None
) -> logging.Logger:
    """
    Get or create a logger for TTS operations.

    :param name: Logger name (typically __name__ from calling module)
    :param level: Logging level (default: WARNING for production)
    :param format_string: Custom format string (optional)
    :return: Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid adding multiple handlers to the same logger
    if not logger.handlers:
        handler = logging.StreamHandler()

        # Use custom format or default
        if format_string is None:
            format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        formatter = logging.Formatter(format_string)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Set level (default to WARNING if not specified)
    if level is not None:
        logger.setLevel(level)
    elif logger.level == logging.NOTSET:
        logger.setLevel(logging.WARNING)

    return logger


def enable_debug_logging(logger_name: str = "test") -> None:
    """
    Enable DEBUG level logging for development/troubleshooting.

    Usage:
        from test.custom_utils import enable_debug_logging
        enable_debug_logging('test.text_to_speech')

    :param logger_name: Name of logger to enable debug for
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)


def disable_logging(logger_name: str = "test") -> None:
    """
    Disable logging (set to CRITICAL only).

    :param logger_name: Name of logger to disable
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.CRITICAL)
