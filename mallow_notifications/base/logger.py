"""Module for defining custom logging functionality.

This module provides a custom logger for the `mallow_notifications` package.

Example:
    To use this module, simply import the defined logger and use it in your code.

    Example:
        from mallow_notifications.base.logger import get_logger

        logger = get_logger(__name__)

Attributes:
    logger: Logger: A logger instance for the `mallow_notifications` package.
"""

import logging


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Returns a logger with the specified name and log level."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    console = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger


loggger = get_logger(__name__)
