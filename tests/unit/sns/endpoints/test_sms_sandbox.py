import unittest
from typing import Optional
from unittest import mock
from unittest.mock import MagicMock, Mock, patch

from botocore.exceptions import ClientError
from faker import Faker
from pydantic_core import ValidationError

from mallow_notifications.base.constants import (
    SMS_SANDBOX_PHONE_NUMBER_STATUS_PENDING,
    SMS_SANDBOX_PHONE_NUMBER_STATUS_VERIFIED,
    SMS_TYPE_PROMOTIONAL,
    SMS_TYPE_TRANSACTIONAL,
)
from mallow_notifications.base.logger import get_logger
from mallow_notifications.base.utils import generate_random_arn
from mallow_notifications.sns import SNSSandboxSMS
from mallow_notifications.sns.endpoints.topics import NotificationError
from mallow_notifications.sns.schema.topics import CreateTopicRequest

faker = Faker()
logging = get_logger(__name__)


class BaseSMSSandBoxTest(unittest.TestCase):
    def setUp(self):
        self.sms = SNSSandboxSMS()
        self.mock_client = MagicMock()
        self.sms.client = self.mock_client
        self.faker = Faker()


class TestGetSMSSandboxAccountStatus(BaseSMSSandBoxTest):
    def test_get_sms_sandbox_account_status_success(self):
        expected_response = {"IsSandboxAccount": True}
        with mock.patch.object(
            self.sms.client,
            "get_sms_sandbox_account_status",
            return_value=expected_response,
        ):
            response = self.sms.get_sms_sandbox_account_status()
            self.assertEqual(response, expected_response)

    def test_get_sms_sandbox_account_status_fail(self):
        expected_response = {"IsSandboxAccount": False}
        with mock.patch.object(
            self.sms.client,
            "get_sms_sandbox_account_status",
            return_value=expected_response,
        ):
            response = self.sms.get_sms_sandbox_account_status()
            self.assertEqual(response, expected_response)

    def test_get_sms_sandbox_account_status_fail_with_client_error(self):
        expected_error = Mock(side_effect=ClientError({}, "get_sms_sandbox_account_status"))
        expected_response = "An error occurred (Unknown) when calling the get_sms_sandbox_account_status operation: Unknown"
        with mock.patch.object(self.sms.client, "get_sms_sandbox_account_status", expected_error):
            with self.assertRaises(NotificationError):
                response = self.sms.get_sms_sandbox_account_status()
                self.assertEqual(response, expected_response)


class TestCreateSMSSandboxPhoneNumber(BaseSMSSandBoxTest):
    def test_create_sms_sandbox_phone_number_success(self):
        sms_sandbox_data = {
            "phone_number": self.faker.phone_number(),
            "language_code": self.faker.pystr(min_chars=1, max_chars=10),
        }
        with mock.patch.object(
            self.sms.client, "create_sms_sandbox_phone_number", return_value=None
        ):
            response = self.sms.create_sms_sandbox_phone_number(sms_sandbox_data)
            self.assertIsNone(response)

    def test_create_sms_sandbox_phone_number_fail_with_client_error(self):
        sms_sandbox_data = {
            "phone_number": self.faker.phone_number(),
            "language_code": self.faker.pystr(min_chars=1, max_chars=10),
        }
        expected_error = Mock(side_effect=ClientError({}, "create_sms_sandbox_phone_number"))
        expected_response = "An error occurred (Unknown) when calling the create_sms_sandbox_phone_number operation: Unknown"
        with mock.patch.object(self.sms.client, "create_sms_sandbox_phone_number", expected_error):
            with self.assertRaises(NotificationError):
                response = self.sms.create_sms_sandbox_phone_number(sms_sandbox_data)
                self.assertEqual(response, expected_response)

    def test_create_sms_sandbox_phone_number_fail_with_validation_error(self):
        sms_sandbox_data = {
            "phone_number": self.faker.random_int(min=1111111111, max=9999999999),
            "language_code": self.faker.random_int(min=1, max=555),
        }
        expected_response = (
            "Validation error in Field 'phone_number' - Input should be a valid string"
        )
        with mock.patch.object(self.sms.client, "create_sms_sandbox_phone_number"):
            with self.assertRaises(NotificationError):
                response = self.sms.create_sms_sandbox_phone_number(sms_sandbox_data)
                self.assertEqual(response, expected_response)


class TestVerifySMSSandboxPhoneNumber(BaseSMSSandBoxTest):
    def test_verify_sms_sandbox_phone_number_success(self):
        phone_number = {
            "phone_number": self.faker.phone_number(),
            "otp": self.faker.pystr(min_chars=1, max_chars=10),
        }
        with mock.patch.object(
            self.sms.client, "verify_sms_sandbox_phone_number", return_value=None
        ):
            response = self.sms.verify_sms_sandbox_phone_number(phone_number)
            self.assertIsNone(response)

    def test_verify_sms_sandbox_phone_number_fail_with_client_error(self):
        phone_number = {
            "phone_number": self.faker.phone_number(),
            "otp": self.faker.pystr(min_chars=1, max_chars=10),
        }
        expected_error = Mock(side_effect=ClientError({}, "verify_sms_sandbox_phone_number"))
        expected_response = "An error occurred (Unknown) when calling the verify_sms_sandbox_phone_number operation: Unknown"
        with mock.patch.object(self.sms.client, "verify_sms_sandbox_phone_number", expected_error):
            with self.assertRaises(NotificationError):
                response = self.sms.verify_sms_sandbox_phone_number(phone_number)
                self.assertEqual(response, expected_response)

    def test_verify_sms_sandbox_phone_number_fail_with_validation_error(self):
        phone_number = {
            "phone_number": self.faker.random_int(min=1111111111, max=9999999999),
            "otp": self.faker.pystr(min_chars=1, max_chars=10),
        }
        expected_response = (
            "Validation error in Field 'phone_number' - Input should be a valid string"
        )
        with mock.patch.object(self.sms.client, "verify_sms_sandbox_phone_number"):
            with self.assertRaises(NotificationError):
                response = self.sms.verify_sms_sandbox_phone_number(phone_number)
                self.assertEqual(response, expected_response)

    def test_verify_sms_sandbox_phone_number_fail_with_invalid_otp(self):
        phone_number = {
            "phone_number": self.faker.phone_number(),
            "otp": self.faker.random_int(min=111111, max=999999),
        }
        expected_response = "Validation error in Field 'otp' - Input should be a valid string"
        with mock.patch.object(self.sms.client, "verify_sms_sandbox_phone_number"):
            with self.assertRaises(NotificationError):
                response = self.sms.verify_sms_sandbox_phone_number(phone_number)
                self.assertEqual(response, expected_response)


class TestDeleteSMSSandboxPhoneNumber(BaseSMSSandBoxTest):
    def test_delete_sms_sandbox_phone_number_success(self):
        phone_number = {"phone_number": self.faker.phone_number()}
        with mock.patch.object(
            self.sms.client, "delete_sms_sandbox_phone_number", return_value=None
        ):
            response = self.sms.delete_sms_sandbox_phone_number(phone_number)
            self.assertIsNone(response)

    def test_delete_sms_sandbox_phone_number_fail_with_client_error(self):
        phone_number = {"phone_number": self.faker.phone_number()}
        expected_error = Mock(side_effect=ClientError({}, "delete_sms_sandbox_phone_number"))
        expected_response = "An error occurred (Unknown) when calling the delete_sms_sandbox_phone_number operation: Unknown"
        with mock.patch.object(self.sms.client, "delete_sms_sandbox_phone_number", expected_error):
            with self.assertRaises(NotificationError):
                response = self.sms.delete_sms_sandbox_phone_number(phone_number)
                self.assertEqual(response, expected_response)

    def test_delete_sms_sandbox_phone_number_fail_with_validation_error(self):
        phone_number = {"phone_number": self.faker.random_int(min=1111111111, max=9999999999)}
        expected_response = (
            "Validation error in Field 'phone_number' - Input should be a valid string"
        )
        with mock.patch.object(self.sms.client, "delete_sms_sandbox_phone_number"):
            with self.assertRaises(NotificationError):
                response = self.sms.delete_sms_sandbox_phone_number(phone_number)
                self.assertEqual(response, expected_response)


class TestListSMSSandboxPhoneNumbers(BaseSMSSandBoxTest):
    def test_list_sms_sandbox_phone_numbers_success(self):
        expected_response = {
            "PhoneNumbers": [
                {
                    "PhoneNumber": self.faker.phone_number(),
                    "Status": self.faker.random_element(
                        [
                            SMS_SANDBOX_PHONE_NUMBER_STATUS_VERIFIED,
                            SMS_SANDBOX_PHONE_NUMBER_STATUS_PENDING,
                        ]
                    ),
                }
            ]
        }
        with mock.patch.object(
            self.sms.client,
            "list_sms_sandbox_phone_numbers",
            return_value=expected_response,
        ):
            response = self.sms.list_sms_sandbox_phone_numbers()
            self.assertEqual(response, expected_response)

    def test_list_sms_sandbox_phone_numbers_success_with_query_params(self):
        expected_response = {
            "PhoneNumbers": [
                {
                    "PhoneNumber": self.faker.phone_number(),
                    "Status": self.faker.random_element(
                        [
                            SMS_SANDBOX_PHONE_NUMBER_STATUS_VERIFIED,
                            SMS_SANDBOX_PHONE_NUMBER_STATUS_PENDING,
                        ]
                    ),
                }
            ]
        }
        query_params = {
            "NextToken": self.faker.pystr(min_chars=1, max_chars=180),
            "MaxResults": self.faker.random_int(min=1, max=10),
        }
        with mock.patch.object(
            self.sms.client,
            "list_sms_sandbox_phone_numbers",
            return_value=expected_response,
        ):
            response = self.sms.list_sms_sandbox_phone_numbers(query_params)
            self.assertEqual(response, expected_response)

    def test_list_sms_sandbox_phone_numbers_success_with__invalid_query_params(self):
        expected_response = (
            "Validation error in Field 'NextToken' - Input should be a valid string"
        )
        query_params = {
            "NextToken": self.faker.random_int(min=1, max=10),
            "MaxResults": self.faker.random_int(min=1, max=10),
        }
        with mock.patch.object(self.sms.client, "list_sms_sandbox_phone_numbers"):
            with self.assertRaises(NotificationError):
                response = self.sms.list_sms_sandbox_phone_numbers(query_params)
                self.assertEqual(response, expected_response)

    def test_list_sms_sandbox_phone_numbers_fail_with_client_error(self):
        expected_error = Mock(side_effect=ClientError({}, "list_sms_sandbox_phone_numbers"))
        expected_response = "An error occurred (Unknown) when calling the list_sms_sandbox_phone_numbers operation: Unknown"
        with mock.patch.object(self.sms.client, "list_sms_sandbox_phone_numbers", expected_error):
            with self.assertRaises(NotificationError):
                response = self.sms.list_sms_sandbox_phone_numbers()
                self.assertEqual(response, expected_response)


class TestGetSMSAttributes(BaseSMSSandBoxTest):
    def test_get_sms_attributes_success(self):
        query_parmas = {"attributes": ["monthly_spend_limit", "default_sms_type"]}

        expected_response = {
            "attributes": {
                "monthly_spend_limit": self.faker.random_int(min=1, max=100),
                "default_sms_type": self.faker.random_element(
                    [SMS_TYPE_PROMOTIONAL, SMS_TYPE_TRANSACTIONAL]
                ),
            }
        }

        with mock.patch.object(
            self.sms.client, "get_sms_attributes", return_value=expected_response
        ):
            response = self.sms.get_sms_attributes(query_parmas)
            self.assertEqual(response, expected_response)

    def test_get_all_sms_attributes(self):
        query_parmas = {
            "attributes": [
                "monthly_spend_limit",
                "delivery_status_iam_role" "delivery_status_success_sampling_rate",
                "default_sender_id",
                "default_sms_type",
                "usage_report_s3_bucket",
            ]
        }
        expected_response = {
            "attributes": {
                "monthly_spend_limit": str(self.faker.random_int(min=1, max=100)),
                "delivery_status_iam_role": self.faker.pystr(min_chars=1, max_chars=100),
                "delivery_status_success_sampling_rate": str(
                    self.faker.random_int(min=1, max=100)
                ),
                "default_sender_id": self.faker.pystr(min_chars=1, max_chars=10),
                "default_sms_type": self.faker.random_element(
                    [SMS_TYPE_PROMOTIONAL, SMS_TYPE_TRANSACTIONAL]
                ),
                "usage_report_s3_bucket": self.faker.pystr(min_chars=1, max_chars=100),
            }
        }

        with mock.patch.object(
            self.sms.client, "get_sms_attributes", return_value=expected_response
        ):
            response = self.sms.get_sms_attributes(query_parmas)
            self.assertEqual(response, expected_response)

    def test_get_sms_attributes_fail_with_client_error(self):
        query_parmas = {"attributes": []}
        expected_error = Mock(side_effect=ClientError({}, "get_sms_attributes"))
        expected_response = (
            "An error occurred (Unknown) when calling the get_sms_attributes operation: Unknown"
        )
        with mock.patch.object(self.sms.client, "get_sms_attributes", expected_error):
            with self.assertRaises(NotificationError):
                response = self.sms.get_sms_attributes(query_parmas)
                self.assertEqual(response, expected_response)


class TestSetSMSAttributes(BaseSMSSandBoxTest):
    def test_set_sms_attributes_success(self):
        query_params = {
            "attributes": {
                "monthly_spend_limit": str(self.faker.random_int(min=1, max=100)),
                "delivery_status_iam_role": self.faker.pystr(min_chars=1, max_chars=100),
                "delivery_status_success_sampling_rate": str(
                    self.faker.random_int(min=1, max=100)
                ),
                "default_sender_id": self.faker.pystr(min_chars=1, max_chars=10),
                "default_sms_type": self.faker.random_element(
                    [SMS_TYPE_PROMOTIONAL, SMS_TYPE_TRANSACTIONAL]
                ),
                "usage_report_s3_bucket": self.faker.pystr(min_chars=1, max_chars=100),
            }
        }

        with mock.patch.object(self.sms.client, "set_sms_attributes", return_value=None):
            response = self.sms.set_sms_attributes(query_params)
            self.assertIsNone(response)

    def test_set_sms_attributes_fail_with_client_error(self):
        query_params = {"attributes": {}}
        expected_error = Mock(side_effect=ClientError({}, "set_sms_attributes"))
        expected_response = (
            "An error occurred (Unknown) when calling the set_sms_attributes operation: Unknown"
        )
        with mock.patch.object(self.sms.client, "set_sms_attributes", expected_error):
            with self.assertRaises(NotificationError):
                response = self.sms.set_sms_attributes(query_params)
                self.assertEqual(response, expected_response)

    def test_set_sms_attributes_fail_with_validation_error(self):
        query_params = {
            "attributes": {
                "monthly_spend_limit": self.faker.random_int(min=1, max=100),
                "delivery_status_iam_role": self.faker.pystr(min_chars=1, max_chars=100),
                "delivery_status_success_sampling_rate": str(
                    self.faker.random_int(min=1, max=100)
                ),
                "default_sender_id": self.faker.pystr(min_chars=1, max_chars=10),
                "default_sms_type": self.faker.random_element(
                    [SMS_TYPE_PROMOTIONAL, SMS_TYPE_TRANSACTIONAL]
                ),
            }
        }
        expected_response = (
            "Validation error in Field 'attributes' - Input should be a valid string"
        )
        with mock.patch.object(self.sms.client, "set_sms_attributes"):
            with self.assertRaises(NotificationError):
                response = self.sms.set_sms_attributes(query_params)
                self.assertEqual(response, expected_response)
