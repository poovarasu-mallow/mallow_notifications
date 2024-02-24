"""Module for configuring and initializing Celery for task management.

This module provides functionality for setting up Celery with the appropriate broker URL
and result backend, using settings from the `Settings` class.
"""

from celery import Celery

from mallow_notifications.base.logger import get_logger
from mallow_notifications.base.settings import Settings

logging = get_logger(__name__)

settings = Settings()

celery = Celery(__name__)


celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND
celery.autodiscover_tasks(
    ["mallow_notifications.mailer.mail_adapter", "mallow_notifications.sns.notification_adpater"]
)
