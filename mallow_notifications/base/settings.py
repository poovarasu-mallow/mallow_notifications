"""Module for defining settings for the `mallow_notifications` package.

This module provides a Settings class that can be used to configure the
Env variables for the package.
"""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings

from mallow_notifications.base.logger import get_logger

logging = get_logger(__name__)


class Settings(BaseSettings):
    """The Settings class configures the environment variables for the
    mallow_notifications package."""

    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: Optional[str] = Field(default="us-east-1")
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    MAIL_DRIVER: Optional[str] = Field(default="log")
    SMTP_MAIL_BACKEND: Optional[str] = None
    SMTP_MAIL_PORT: Optional[int] = None
    SMTP_MAIL_USERNAME: Optional[str] = None
    SMTP_MAIL_PASSWORD: Optional[str] = None
    SMTP_MAIL_USE_SSL: Optional[bool] = False

    class Config:
        """Pydantic configuration for the Settings class."""

        env_file = ".env"
        extra = "allow"
