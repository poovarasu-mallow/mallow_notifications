"""This module contains the `SNSPushNotification` class for sending SNS
messages.

This module provides functionality for sending SNS messages using the
boto3 AWS SDK for Python.
"""

from typing import Dict, Optional, Union

from botocore.exceptions import ClientError
from pydantic import ValidationError

from mallow_notifications.base.logger import get_logger
from mallow_notifications.base.utils import NotificationError, handle_validation_error
from mallow_notifications.sns.endpoints import SNSClient
from mallow_notifications.sns.schema.base import NextToken
from mallow_notifications.sns.schema.push_notification import (
    GetEndpointAttributesResponse,
    ListPlatformApplications,
    PlatformApplicationArnSchema,
    PlatformApplicationRequest,
    PlatformEndpointRequest,
    PlatformEndpointSchema,
)

logger = get_logger(__name__)


class SNSPushNotification(SNSClient):
    """Class for sending SNS messages using the boto3 AWS SDK for Python."""

    def __init__(self):
        super().__init__()

    def create_platform_application(
        self, platform_data: Union[PlatformApplicationRequest, Dict[str, any]]
    ) -> PlatformApplicationArnSchema:
        """Creates a platform application object for one of the supported push
        notification services."""
        try:
            data = PlatformApplicationRequest.process_input(platform_data)
            response = self.client.create_platform_application(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.InvalidParameterException,
        ) as e:
            raise NotificationError(e)

    def delete_platform_application(
        self, platform_arn: Union[PlatformApplicationArnSchema, Dict[str, str]]
    ):
        """Deletes a platform application object for one of the supported push
        notification services."""
        try:
            data = PlatformApplicationArnSchema.process_input(platform_arn)
            response = self.client.delete_platform_application(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.InvalidParameterException,
        ) as e:
            raise NotificationError(e)

    # pylint: disable=dangerous-default-value
    def list_platform_applications(
        self, next_token: Optional[Union[NextToken, Dict[str, any]]] = {"NextToken": None}
    ) -> ListPlatformApplications:
        """Lists the platform application objects for one of the supported push
        notification services."""
        try:
            data = NextToken.process_input(next_token)
            response = self.client.list_platform_applications(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.InvalidParameterException,
        ) as e:
            raise NotificationError(e)

    def create_platform_endpoint(
        self, endpoint_data: Union[PlatformEndpointRequest, Dict[str, any]]
    ) -> PlatformEndpointSchema:
        """Creates an endpoint for one of the supported push notification
        services."""
        try:
            data = PlatformEndpointRequest.process_input(endpoint_data)
            response = self.client.create_platform_endpoint(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.NotFoundException,
        ) as e:
            raise NotificationError(e)

    def delete_platform_endpoint(
        self, endpoint_arn: Union[PlatformEndpointSchema, Dict[str, str]]
    ):
        """Deletes the endpoint for a device and mobile app from Amazon SNS
        Platform Application."""
        try:
            data = PlatformEndpointSchema.process_input(endpoint_arn)
            response = self.client.delete_endpoint(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.InvalidParameterException,
        ) as e:
            raise NotificationError(e)

    def list_endpoints_by_platform_application(
        self, platform_arn: Union[PlatformApplicationArnSchema, Dict[str, str]]
    ) -> ListPlatformApplications:
        """Lists the endpoints and endpoint attributes for one of the supported
        push notification services."""
        try:
            data = PlatformApplicationArnSchema.process_input(platform_arn)
            response = self.client.list_endpoints_by_platform_application(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.NotFoundException,
        ) as e:
            raise NotificationError(e)

    def get_endpoint_attributes(
        self, endpoint_arn: Union[PlatformEndpointSchema, Dict[str, str]]
    ) -> GetEndpointAttributesResponse:
        """Returns the endpoint attributes for a device and mobile app."""
        try:
            data = PlatformEndpointSchema.process_input(endpoint_arn)
            response = self.client.get_endpoint_attributes(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.NotFoundException,
        ) as e:
            raise NotificationError(e)
