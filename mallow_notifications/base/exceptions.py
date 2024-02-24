"""Module for defining custom exceptions related to notifications and mailing
errors.

This module provides custom exception classes for handling various errors that may
occur during notification sending and mailing processes.

Example:
    To use this module, simply import the defined exception classes and use them
    where appropriate in your code.

    Example:
        from mallow_notifications.base.exceptions import (
            NotificationError,
            MailError,
        )

Attributes:
    NotificationError: Exception: An exception raised for generic notification errors.
    MailError: Exception: An exception raised for generic mail errors.
"""

from mallow_notifications.base.logger import get_logger

logging = get_logger(__name__)


class NotificationError(Exception):
    """Exception raised for Amazon SNS notification errors."""


class MailError(BaseException):
    """Exception raised for mail errors."""
