import unittest
from typing import Optional
from unittest import mock
from unittest.mock import MagicMock, Mock, patch

from botocore.exceptions import ClientError
from faker import Faker

from mallow_notifications.base.logger import get_logger
from mallow_notifications.base.utils import generate_random_arn
from mallow_notifications.sns import SNSPushNotification
from mallow_notifications.sns.endpoints.topics import NotificationError
from mallow_notifications.sns.schema.push_notification import Platforms
from mallow_notifications.sns.schema.topics import CreateTopicRequest

faker = Faker()
logging = get_logger(__name__)


class BasePushNotificationTest(unittest.TestCase):
    def setUp(self):
        self.push_notification = SNSPushNotification()
        self.mock_client = MagicMock()
        self.push_notification.client = self.mock_client
        self.faker = Faker()


class TestCreatePlatformApplication(BasePushNotificationTest):
    def test_create_platform_application_success_response(self):
        platform_application_data = {
            "platform_name": self.faker.pystr(min_chars=1, max_chars=180),
            "platform_type": self.faker.random_element(Platforms),
        }
        expected_response = {
            "PlatformApplicationArn": generate_random_arn(
                self.faker, platform_application_data["platform_name"]
            )
        }
        with mock.patch.object(
            self.push_notification.client,
            "create_platform_application",
            return_value=expected_response,
        ):
            response = self.push_notification.create_platform_application(
                platform_application_data
            )
            self.assertEqual(response, expected_response)

    def test_create_platform_application_success_with_all_fields(self):
        platform_application_data = {
            "platform_name": self.faker.pystr(min_chars=1, max_chars=180),
            "platform_type": self.faker.random_element(Platforms),
            "platform_attributes": {
                "platform_principal": self.faker.pystr(min_chars=1, max_chars=256),
                "platform_credential": self.faker.pystr(min_chars=1, max_chars=256),
                "event_endpoint_created": generate_random_arn(
                    self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                ),
                "event_endpoint_update": generate_random_arn(
                    self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                ),
                "event_endpoint_deleted": generate_random_arn(
                    self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                ),
                "event_delivery_failure": generate_random_arn(
                    self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                ),
                "success_feedback_role_arn": generate_random_arn(
                    self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                ),
                "failure_feedback_role_arn": generate_random_arn(
                    self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                ),
                "success_feedback_sample_rate": self.faker.random_int(min=1, max=100),
            },
        }
        expected_response = {
            "PlatformApplicationArn": generate_random_arn(
                self.faker, platform_application_data["platform_name"]
            )
        }
        with mock.patch.object(
            self.push_notification.client,
            "create_platform_application",
            return_value=expected_response,
        ):
            response = self.push_notification.create_platform_application(
                platform_application_data
            )
            self.assertEqual(response, expected_response)

    def test_create_platform_application_client_error(self):
        platform_application_data = {
            "platform_name": self.faker.pystr(min_chars=1, max_chars=180),
            "platform_type": self.faker.random_element(Platforms),
        }
        expected_error = Mock(side_effect=ClientError({}, "create_platform_application"))
        expected_response = "An error occurred (Unknown) when calling the create_platform_application operation: Unknown"
        with mock.patch.object(
            self.push_notification.client, "create_platform_application", expected_error
        ):
            with self.assertRaises(NotificationError):
                response = self.push_notification.create_platform_application(
                    platform_application_data
                )
                self.assertEqual(response, expected_response)

    def test_create_platform_application_validation_error(self):
        platform_application_data = {
            "platform_name": self.faker.pystr(min_chars=1, max_chars=180),
            "platform_type": self.faker.pystr(min_chars=1, max_chars=180),
        }
        expected_response = "Validation error in Field 'platform_type' - Input should be 'ADM', 'Baidu', 'APNS', 'APNS_SANDBOX', 'GCM', 'MPNS' or 'WNS'"
        with mock.patch.object(self.push_notification.client, "create_platform_application"):
            with self.assertRaises(NotificationError):
                response = self.push_notification.create_platform_application(
                    platform_application_data
                )
                self.assertEqual(response, expected_response)


class TestDeletePlatformApplication(BasePushNotificationTest):
    def test_delete_platform_application_success_response(self):
        platform_arn = {
            "platform_application_arn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
            )
        }
        with mock.patch.object(
            self.push_notification.client,
            "delete_platform_application",
            return_value=None,
        ):
            response = self.push_notification.delete_platform_application(platform_arn)
            self.assertIsNone(response)

    def test_delete_platform_application_client_error(self):
        platform_arn = {
            "platform_application_arn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
            )
        }
        expected_error = Mock(side_effect=ClientError({}, "delete_platform_application"))
        expected_response = "An error occurred (Unknown) when calling the delete_platform_application operation: Unknown"
        with mock.patch.object(
            self.push_notification.client, "delete_platform_application", expected_error
        ):
            with self.assertRaises(NotificationError):
                response = self.push_notification.delete_platform_application(platform_arn)
                self.assertEqual(response, expected_response)

    def test_delete_platform_application_validation_error(self):
        platform_arn = {
            "platform_application_arn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=260, max_chars=270)
            )
        }
        expected_response = f"Validation error in Field 'platform_application_arn' - Value should have at most 256 items after validation, not {len(platform_arn['platform_application_arn'])}"
        with mock.patch.object(self.push_notification.client, "delete_platform_application"):
            with self.assertRaises(NotificationError):
                response = self.push_notification.delete_platform_application(platform_arn)
                self.assertEqual(response, expected_response)


class TestListPlatformApplication(BasePushNotificationTest):
    def test_list_platform_applications_success_response(self):
        expected_response = {
            "PlatformApplications": [
                {
                    "PlatformApplicationArn": generate_random_arn(
                        self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                    ),
                    "Attributes": {},
                }
            ]
        }

        with mock.patch.object(
            self.push_notification.client,
            "list_platform_applications",
            return_value=expected_response,
        ):
            response = self.push_notification.list_platform_applications()
            self.assertEqual(response, expected_response)

    def test_list_platform_applications_with_next_token(self):
        next_token = {"NextToken": self.faker.pystr(min_chars=1, max_chars=100)}
        expected_response = {
            "PlatformApplications": [
                {
                    "PlatformApplicationArn": generate_random_arn(
                        self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                    ),
                    "Attributes": {},
                }
            ],
            "NextToken": self.faker.pystr(min_chars=1, max_chars=100),
        }

        with mock.patch.object(
            self.push_notification.client,
            "list_platform_applications",
            return_value=expected_response,
        ):
            response = self.push_notification.list_platform_applications(next_token)
            self.assertEqual(response, expected_response)

    def test_list_platform_applications_client_error(self):
        expected_error = Mock(side_effect=ClientError({}, "list_platform_applications"))
        expected_response = "An error occurred (Unknown) when calling the list_platform_applications operation: Unknown"
        with mock.patch.object(
            self.push_notification.client, "list_platform_applications", expected_error
        ):
            with self.assertRaises(NotificationError):
                response = self.push_notification.list_platform_applications()
                self.assertEqual(response, expected_response)

    def test_list_platform_application_validation_error(self):
        next_token = {"NextToken": self.faker.random_int(min=1, max=100)}
        expected_response = (
            "Validation error in Field 'NextToken' - Input should be a valid string"
        )
        with mock.patch.object(self.push_notification.client, "list_platform_applications"):
            with self.assertRaises(NotificationError):
                response = self.push_notification.list_platform_applications(next_token)
                self.assertEqual(response, expected_response)


class TestCreatePlatformEndpoint(BasePushNotificationTest):
    def test_create_platform_endpoint_success_response(self):
        endpoint_data = {
            "platform_application_arn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
            ),
            "device_token": self.faker.pystr(min_chars=1, max_chars=256),
        }
        expected_response = {
            "EndpointArn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
            )
        }
        with mock.patch.object(
            self.push_notification.client,
            "create_platform_endpoint",
            return_value=expected_response,
        ):
            response = self.push_notification.create_platform_endpoint(endpoint_data)
            self.assertEqual(response, expected_response)

    def test_create_platform_endpoint__with_all_attributes(self):
        endpoint_data = {
            "platform_application_arn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
            ),
            "device_token": self.faker.pystr(min_chars=1, max_chars=256),
            "custom_user_data": self.faker.pystr(min_chars=1, max_chars=256),
        }
        expected_response = {
            "EndpointArn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
            )
        }
        with mock.patch.object(
            self.push_notification.client,
            "create_platform_endpoint",
            return_value=expected_response,
        ):
            response = self.push_notification.create_platform_endpoint(endpoint_data)
            self.assertEqual(response, expected_response)

    def test_create_platform_endpoint_client_error(self):
        endpoint_data = {
            "platform_application_arn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
            ),
            "device_token": self.faker.pystr(min_chars=1, max_chars=256),
        }
        expected_error = Mock(side_effect=ClientError({}, "create_platform_endpoint"))
        expected_response = "An error occurred (Unknown) when calling the create_platform_endpoint operation: Unknown"
        with mock.patch.object(
            self.push_notification.client, "create_platform_endpoint", expected_error
        ):
            with self.assertRaises(NotificationError):
                response = self.push_notification.create_platform_endpoint(endpoint_data)
                self.assertEqual(response, expected_response)

    def test_create_platform_endpoint_validation_error(self):
        endpoint_data = {
            "platform_application_arn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
            ),
            "device_token": self.faker.random_int(),
        }
        expected_response = (
            "alidation error in Field 'device_token' - Input should be a valid string"
        )
        with mock.patch.object(self.push_notification.client, "create_platform_endpoint"):
            with self.assertRaises(NotificationError):
                response = self.push_notification.create_platform_endpoint(endpoint_data)
                self.assertEqual(response, expected_response)


class TestDeletePlatformEndpoint(BasePushNotificationTest):
    def test_delete_platform_endpoint_success_response(self):
        endpoint_arn = {
            "endpoint_arn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
            )
        }
        with mock.patch.object(
            self.push_notification.client, "delete_endpoint", return_value=None
        ):
            response = self.push_notification.delete_platform_endpoint(endpoint_arn)
            self.assertIsNone(response)

    def test_delete_platform_endpoint_client_error(self):
        endpoint_arn = {
            "endpoint_arn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
            )
        }
        expected_error = Mock(side_effect=ClientError({}, "delete_endpoint"))
        expected_response = (
            "An error occurred (Unknown) when calling the delete_endpoint operation: Unknown"
        )
        with mock.patch.object(self.push_notification.client, "delete_endpoint", expected_error):
            with self.assertRaises(NotificationError):
                response = self.push_notification.delete_platform_endpoint(endpoint_arn)
                self.assertEqual(response, expected_response)

    def test_delete_platform_endpoint_validation_error(self):
        endpoint_arn = {"endpoint_arn": self.faker.random_int()}
        expected_response = (
            "Validation error in Field 'endpoint_arn' - Input should be a valid string"
        )
        with mock.patch.object(self.push_notification.client, "delete_endpoint"):
            with self.assertRaises(NotificationError):
                response = self.push_notification.delete_platform_endpoint(endpoint_arn)
                self.assertEqual(response, expected_response)


class TestListPlatformEndpoints(BasePushNotificationTest):
    def test_list_endpoints_by_platform_application_success_response(self):
        platform_application_arn = {
            "platform_application_arn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
            )
        }
        expected_response = {
            "Endpoints": [
                {
                    "EndpointArn": generate_random_arn(
                        self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                    ),
                    "Attributes": {},
                }
            ]
        }
        with mock.patch.object(
            self.push_notification.client,
            "list_endpoints_by_platform_application",
            return_value=expected_response,
        ):
            response = self.push_notification.list_endpoints_by_platform_application(
                platform_application_arn
            )
            self.assertEqual(response, expected_response)

    def test_list_endpoints_by_platform_application_with_next_token(self):
        platform_application_arn = {
            "platform_application_arn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
            ),
            "NextToken": self.faker.pystr(min_chars=1, max_chars=100),
        }
        expected_response = {
            "Endpoints": [
                {
                    "EndpointArn": generate_random_arn(
                        self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                    ),
                    "Attributes": {},
                }
            ],
            "NextToken": self.faker.pystr(min_chars=1, max_chars=100),
        }
        with mock.patch.object(
            self.push_notification.client,
            "list_endpoints_by_platform_application",
            return_value=expected_response,
        ):
            response = self.push_notification.list_endpoints_by_platform_application(
                platform_application_arn
            )
            self.assertEqual(response, expected_response)

    def test_list_endpoints_by_platform_application_client_error(self):
        platform_application_arn = {
            "platform_application_arn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
            )
        }
        expected_error = Mock(
            side_effect=ClientError({}, "list_endpoints_by_platform_application")
        )
        expected_response = "An error occurred (Unknown) when calling the list_endpoints_by_platform_application operation: Unknown"
        with mock.patch.object(
            self.push_notification.client,
            "list_endpoints_by_platform_application",
            expected_error,
        ):
            with self.assertRaises(NotificationError):
                response = self.push_notification.list_endpoints_by_platform_application(
                    platform_application_arn
                )
                self.assertEqual(response, expected_response)

    def test_list_endpoints_by_platform_application_validation_error(self):
        platform_application_arn = {"platform_application_arn": self.faker.random_int()}
        expected_response = (
            "Validation error in Field 'platform_application_arn' - Input should be a valid string"
        )
        with mock.patch.object(
            self.push_notification.client, "list_endpoints_by_platform_application"
        ):
            with self.assertRaises(NotificationError):
                response = self.push_notification.list_endpoints_by_platform_application(
                    platform_application_arn
                )
                self.assertEqual(response, expected_response)


class TestGetEndpointAttributes(BasePushNotificationTest):
    def test_get_endpoint_attributes_success_response(self):
        endpoint_arn = {
            "endpoint_arn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
            )
        }
        expected_response = {
            "Attributes": {
                "Enabled": "true",
                "Token": self.faker.pystr(min_chars=1, max_chars=1024),
            }
        }
        with mock.patch.object(
            self.push_notification.client,
            "get_endpoint_attributes",
            return_value=expected_response,
        ):
            response = self.push_notification.get_endpoint_attributes(endpoint_arn)
            self.assertEqual(response, expected_response)

    def test_get_endpoint_attributes_invalid_ar(self):
        endpoint_arn = {
            "endpoint_arn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=270, max_chars=280)
            )
        }
        expected_response = [
            "Validation error in Field 'endpoint_arn' - String should have at most 256 characters"
        ]
        with mock.patch.object(self.push_notification.client, "get_endpoint_attributes"):
            with self.assertRaises(NotificationError):
                response = self.push_notification.get_endpoint_attributes(endpoint_arn)
                self.assertEqual(response, expected_response)

    def test_get_endpoint_attributes_client_error(self):
        endpoint_arn = {
            "endpoint_arn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
            )
        }
        expected_error = Mock(side_effect=ClientError({}, "get_endpoint_attributes"))
        expected_response = "An error occurred (Unknown) when calling the get_endpoint_attributes operation: Unknown"
        with mock.patch.object(
            self.push_notification.client, "get_endpoint_attributes", expected_error
        ):
            with self.assertRaises(NotificationError):
                response = self.push_notification.get_endpoint_attributes(endpoint_arn)
                self.assertEqual(response, expected_response)
