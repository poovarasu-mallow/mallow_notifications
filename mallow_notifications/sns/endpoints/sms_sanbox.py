"""This module contains the `SNSSandboxSMS` class for sending SNS messages.

This module provides functionality for sending SNS messages using the
boto3 AWS SDK for Python.
"""

from typing import Dict, List, Optional, Union

from botocore.exceptions import ClientError
from pydantic import ValidationError

from mallow_notifications.base.logger import get_logger
from mallow_notifications.base.utils import NotificationError, handle_validation_error
from mallow_notifications.sns.endpoints import SNSClient
from mallow_notifications.sns.schema.sms_sandbox import (
    CreateSmsSandboxPhoneNumberRequest,
    GetSMSAttributesResponse,
    ListSmsSandboxPhoneNumbersRequest,
    ListSmsSandboxPhoneNumbersResponse,
    SetSMSAttributesRequest,
    SMSPhoneNumber,
    VerifySMSSandboxPhoneNumberRequest,
)

logger = get_logger(__name__)


class SNSSandboxSMS(SNSClient):
    """Class for sending SNS messages using the boto3 AWS SDK for Python."""

    def __init__(self):
        super().__init__()

    def get_sms_sandbox_account_status(self) -> dict:
        """Retrieves the SMS sandbox status for the calling Amazon Web Services
        account in the target Amazon Web Services Region."""
        try:
            response = self.client.get_sms_sandbox_account_status()
            return response
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.ThrottledException,
        ) as e:
            raise NotificationError(e)

    def create_sms_sandbox_phone_number(
        self,
        sms_sandbox_data: Union[CreateSmsSandboxPhoneNumberRequest, Dict[str, any]],
    ) -> dict:
        """Adds a destination phone number to an Amazon Web Services account in
        the SMS sandbox and sends a one-time password (OTP) to that phone
        number."""
        try:
            data = CreateSmsSandboxPhoneNumberRequest.process_input(sms_sandbox_data)
            response = self.client.create_sms_sandbox_phone_number(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.OptedOutException,
            self.client.exceptions.UserErrorException,
            self.client.exceptions.ThrottledException,
        ) as e:
            raise NotificationError(e)

    def verify_sms_sandbox_phone_number(
        self,
        verify_sms_sandbox_phone_number: Union[VerifySMSSandboxPhoneNumberRequest, Dict[str, str]],
    ) -> dict:
        """Verifies an OTP sent to a destination phone number in the SMS
        sandbox."""
        try:
            data = VerifySMSSandboxPhoneNumberRequest.process_input(
                verify_sms_sandbox_phone_number
            )
            response = self.client.verify_sms_sandbox_phone_number(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.ResourceNotFoundException,
            self.client.exceptions.VerificationException,
            self.client.exceptions.ThrottledException,
        ) as e:
            raise NotificationError(e)

    def delete_sms_sandbox_phone_number(
        self, phone_number: Union[SMSPhoneNumber, Dict[str, str]]
    ) -> dict:
        """Deletes an Amazon Web Services account's verified or pending phone
        number from the SMS sandbox."""
        try:
            data = SMSPhoneNumber.process_input(phone_number)
            response = self.client.delete_sms_sandbox_phone_number(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.ResourceNotFoundException,
            self.client.exceptions.UserErrorException,
            self.client.exceptions.ThrottledException,
        ) as e:
            raise NotificationError(e)

    # pylint: disable=dangerous-default-value
    def list_sms_sandbox_phone_numbers(
        self,
        next_token_data: Optional[Union[ListSmsSandboxPhoneNumbersRequest, Dict[str, any]]] = {
            "NextToken": None
        },
    ) -> ListSmsSandboxPhoneNumbersResponse:
        """Lists the calling Amazon Web Services account's current verified and
        pending destination phone numbers in the SMS sandbox."""
        try:
            data = ListSmsSandboxPhoneNumbersRequest.process_input(next_token_data)
            response = self.client.list_sms_sandbox_phone_numbers(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.ResourceNotFoundException,
            self.client.exceptions.ThrottledException,
        ) as e:
            raise NotificationError(e)

    def get_sms_attributes(self, attributes: List[str]) -> GetSMSAttributesResponse:
        """Returns the settings for sending SMS messages from your Amazon Web
        Services account."""
        try:
            response = self.client.get_sms_attributes(attributes=attributes)
            return response
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.ThrottledException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InvalidParameterException,
        ) as e:
            raise NotificationError(e)

    def set_sms_attributes(
        self, attributes: Union[SetSMSAttributesRequest, Dict[str, any]]
    ) -> Dict:
        """Set the default settings for sending SMS messages and receiving
        daily SMS usage reports."""
        try:
            data = SetSMSAttributesRequest.process_input(attributes)
            # logger.critical
            response = self.client.set_sms_attributes(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.ThrottledException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.AuthorizationErrorException,
        ) as e:
            raise NotificationError(e)
