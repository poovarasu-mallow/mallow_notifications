"""This module contains the `SNSClient` class for sending SNS messages.

This module provides functionality for sending SNS messages using the
boto3 AWS SDK
"""

from typing import Union

import boto3
from pydantic import BaseModel

from mallow_notifications.base.constants import AmazonSerives
from mallow_notifications.base.settings import Settings

settings = Settings()


class SNSClient:
    """Class for sending SNS messages using the boto3 AWS SDK for Python."""

    def __init__(self):
        self.client = boto3.client(
            AmazonSerives.SNS,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
