"""This module contains the `SNSPublishMessage` class for sending SNS messages.

This module provides functionality for sending SNS messages using the
boto3 AWS SDK for Python.
"""

from typing import Dict, Union

from botocore.exceptions import ClientError
from pydantic import ValidationError

from mallow_notifications.base.logger import get_logger
from mallow_notifications.base.utils import NotificationError, handle_validation_error
from mallow_notifications.sns.endpoints import SNSClient
from mallow_notifications.sns.schema.publish import (
    PublishBatchRequest,
    PublishBatchResponse,
    PublishRequest,
    PublishResponse,
)

logger = get_logger(__name__)


class SNSPublishMessage(SNSClient):
    """Class for sending SNS messages using the boto3 AWS SDK for Python."""

    def __init__(self):
        super().__init__()

    # pylint: disable=raise-missing-from
    def publish(self, publish_request: Union[PublishRequest, Dict[str, any]]) -> PublishResponse:
        """Sends a message to an Amazon SNS topic, a text message (SMS message)
        directly to a phone number, or a message to a mobile platform endpoint
        (when you specify the TargetArn)."""
        try:
            data = PublishRequest.process_input(publish_request)
            response = self.client.publish(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.InvalidParameterValueException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.NotFoundException,
            self.client.exceptions.EndpointDisabledException,
            self.client.exceptions.PlatformApplicationDisabledException,
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.KMSDisabledException,
            self.client.exceptions.KMSInvalidStateException,
            self.client.exceptions.KMSNotFoundException,
            self.client.exceptions.KMSOptInRequired,
            self.client.exceptions.KMSThrottlingException,
            self.client.exceptions.KMSAccessDeniedException,
            self.client.exceptions.InvalidSecurityException,
            self.client.exceptions.ValidationException,
        ) as e:
            raise NotificationError(e)

    # pylint: disable=raise-missing-from
    def publish_batch(
        self, publish_batch_request: Union[PublishBatchRequest, Dict[str, any]]
    ) -> PublishBatchResponse:
        """Publishes up to ten messages to the specified topic.

        This is a batch version of Publish. For FIFO topics, multiple
        messages within a single batch are published in the order they
        are sent, and messages are deduplicated within the batch and
        across batches for 5 minutes.
        """
        try:
            data = PublishBatchRequest.process_input(publish_batch_request)
            response = self.client.publish_batch(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.InvalidParameterValueException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.NotFoundException,
            self.client.exceptions.EndpointDisabledException,
            self.client.exceptions.PlatformApplicationDisabledException,
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.BatchEntryIdsNotDistinctException,
            self.client.exceptions.BatchRequestTooLongException,
            self.client.exceptions.EmptyBatchRequestException,
            self.client.exceptions.InvalidBatchEntryIdException,
            self.client.exceptions.TooManyEntriesInBatchRequestException,
            self.client.exceptions.KMSDisabledException,
            self.client.exceptions.KMSInvalidStateException,
            self.client.exceptions.KMSNotFoundException,
            self.client.exceptions.KMSOptInRequired,
            self.client.exceptions.KMSThrottlingException,
            self.client.exceptions.KMSAccessDeniedException,
            self.client.exceptions.InvalidSecurityException,
            self.client.exceptions.ValidationException,
        ) as e:
            raise NotificationError(e)
