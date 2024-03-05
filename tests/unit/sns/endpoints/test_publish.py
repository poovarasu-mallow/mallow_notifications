import unittest
from typing import Optional
from unittest import mock
from unittest.mock import MagicMock, Mock, patch

from botocore.exceptions import ClientError
from faker import Faker
from pydantic_core import ValidationError

from mallow_notifications.base.logger import get_logger
from mallow_notifications.base.utils import generate_random_arn
from mallow_notifications.sns import SNSPublishMessage
from mallow_notifications.sns.endpoints.topics import NotificationError
from mallow_notifications.sns.schema.publish import MessageAttributeDataTypes
from mallow_notifications.sns.schema.topics import CreateTopicRequest

faker = Faker()
logging = get_logger(__name__)


class BasePublishTest(unittest.TestCase):
    def setUp(self):
        self.publish = SNSPublishMessage()
        self.mock_client = MagicMock()
        self.publish.client = self.mock_client
        self.faker = Faker()


class TestPublish(BasePublishTest):
    def test_publish_success_response(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        message_data = {
            "topic_arn": generate_random_arn(self.faker, name),
            "subject": self.faker.pystr(min_chars=1, max_chars=256),
            "message": self.faker.pystr(min_chars=1, max_chars=256),
        }
        expected_response = {"MessageId": self.faker.pystr(min_chars=1, max_chars=256)}
        with mock.patch.object(self.publish.client, "publish", return_value=expected_response):
            response = self.publish.publish(message_data)
            self.assertEqual(response, expected_response)

    def test_publish_success_with_all_fields(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        message_data = {
            "topic_arn": generate_random_arn(self.faker, name),
            "subject": self.faker.pystr(min_chars=1, max_chars=256),
            "message": self.faker.pystr(min_chars=1, max_chars=256),
            "message_attributes": {
                self.faker.pystr(min_chars=1, max_chars=20): {
                    "data_type": self.faker.random_element(MessageAttributeDataTypes),
                    "string_value": self.faker.pystr(min_chars=1, max_chars=256),
                }
            },
            "message_deduplication_id": self.faker.pystr(min_chars=1, max_chars=128),
            "message_group_id": self.faker.pystr(min_chars=1, max_chars=128),
        }
        expected_response = {"MessageId": self.faker.pystr(min_chars=1, max_chars=256)}
        with mock.patch.object(self.publish.client, "publish", return_value=expected_response):
            response = self.publish.publish(message_data)
            self.assertEqual(response, expected_response)

    def test_publish_invalid_input(self):
        name = self.faker.pystr(min_chars=260, max_chars=300)
        message_data = {
            "topic_arn": generate_random_arn(self.faker, name),
            "subject": self.faker.pystr(min_chars=1, max_chars=256),
            "message": self.faker.pystr(min_chars=1, max_chars=256),
            "message_attributes": {
                self.faker.pystr(min_chars=1, max_chars=20): {
                    "data_type": self.faker.random_element(MessageAttributeDataTypes),
                    "string_value": self.faker.pystr(min_chars=1, max_chars=256),
                }
            },
            "message_deduplication_id": self.faker.pystr(min_chars=1, max_chars=256),
            "message_group_id": self.faker.pystr(min_chars=1, max_chars=256),
        }
        expected_response = f"Validation error in Field 'topic_arn' - Value should have at most 256 items after validation, not {message_data.get('topic_arn')}"
        with mock.patch.object(self.publish.client, "publish"):
            with self.assertRaises(NotificationError):
                response = self.publish.publish(message_data)
                self.assertEqual(response, expected_response)

    def test_publish_client_error(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        message_data = {
            "topic_arn": generate_random_arn(self.faker, name),
            "subject": self.faker.pystr(min_chars=1, max_chars=256),
            "message": self.faker.pystr(min_chars=1, max_chars=256),
        }
        expected_error = Mock(side_effect=ClientError({}, "get_subscription_attributes"))
        expected_response = "An error occurred (Unknown) when calling the get_subscription_attributes operation: Unknown"
        with mock.patch.object(self.publish.client, "publish", expected_error):
            with self.assertRaises(NotificationError):
                response = self.publish.publish(message_data)
                self.assertEqual(response, expected_response)


class TestPublishBatch(BasePublishTest):
    def test_publish_batch_success_response(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        message_data = {
            "topic_arn": generate_random_arn(self.faker, name),
            "publish_batch_request_entries": [
                {
                    "id": self.faker.pystr(min_chars=1, max_chars=100),
                    "message": self.faker.pystr(min_chars=1, max_chars=256),
                    "subject": self.faker.pystr(min_chars=1, max_chars=256),
                    "message_attributes": {
                        self.faker.pystr(min_chars=1, max_chars=20): {
                            "data_type": self.faker.random_element(MessageAttributeDataTypes),
                            "string_value": self.faker.pystr(min_chars=1, max_chars=256),
                        }
                    },
                    "message_deduplication_id": self.faker.pystr(min_chars=1, max_chars=128),
                    "message_group_id": self.faker.pystr(min_chars=1, max_chars=128),
                }
            ],
        }
        expected_response = {
            "Successful": [
                {
                    "Id": message_data["publish_batch_request_entries"][0]["id"],
                    "MessageId": self.faker.pystr(min_chars=1, max_chars=256),
                    "SequenceNumber": self.faker.pystr(min_chars=1, max_chars=100),
                },
            ]
        }
        with mock.patch.object(
            self.publish.client, "publish_batch", return_value=expected_response
        ):
            response = self.publish.publish_batch(message_data)
            self.assertEqual(response, expected_response)

    def test_publish_batch_multiple_message(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        message_data = {
            "topic_arn": generate_random_arn(self.faker, name),
            "publish_batch_request_entries": [
                {
                    "id": self.faker.pystr(min_chars=1, max_chars=100),
                    "message": self.faker.pystr(min_chars=1, max_chars=256),
                    "subject": self.faker.pystr(min_chars=1, max_chars=256),
                    "message_attributes": {
                        self.faker.pystr(min_chars=1, max_chars=20): {
                            "data_type": self.faker.random_element(MessageAttributeDataTypes),
                            "string_value": self.faker.pystr(min_chars=1, max_chars=256),
                        }
                    },
                    "message_deduplication_id": self.faker.pystr(min_chars=1, max_chars=128),
                    "message_group_id": self.faker.pystr(min_chars=1, max_chars=128),
                },
                {
                    "id": self.faker.pystr(min_chars=1, max_chars=100),
                    "message": self.faker.pystr(min_chars=1, max_chars=256),
                    "subject": self.faker.pystr(min_chars=1, max_chars=256),
                    "message_attributes": {
                        self.faker.pystr(min_chars=1, max_chars=20): {
                            "data_type": self.faker.random_element(MessageAttributeDataTypes),
                            "string_value": self.faker.pystr(min_chars=1, max_chars=256),
                        }
                    },
                    "message_deduplication_id": self.faker.pystr(min_chars=1, max_chars=128),
                    "message_group_id": self.faker.pystr(min_chars=1, max_chars=128),
                },
            ],
        }
        expected_response = {
            "Successful": [
                {
                    "Id": message_data["publish_batch_request_entries"][0]["id"],
                    "MessageId": self.faker.pystr(min_chars=1, max_chars=256),
                    "SequenceNumber": self.faker.pystr(min_chars=1, max_chars=100),
                },
                {
                    "Id": message_data["publish_batch_request_entries"][1]["id"],
                    "MessageId": self.faker.pystr(min_chars=1, max_chars=256),
                    "SequenceNumber": self.faker.pystr(min_chars=1, max_chars=100),
                },
            ]
        }
        with mock.patch.object(
            self.publish.client, "publish_batch", return_value=expected_response
        ):
            response = self.publish.publish_batch(message_data)
            self.assertEqual(response, expected_response)
            self.assertEqual(len(response["Successful"]), 2)

    def test_publish_batch_with_failed_message(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        message_data = {
            "topic_arn": generate_random_arn(self.faker, name),
            "publish_batch_request_entries": [
                {
                    "id": self.faker.pystr(min_chars=1, max_chars=100),
                    "message": self.faker.pystr(min_chars=1, max_chars=256),
                    "subject": self.faker.pystr(min_chars=1, max_chars=256),
                    "message_attributes": {
                        self.faker.pystr(min_chars=1, max_chars=20): {
                            "data_type": self.faker.random_element(MessageAttributeDataTypes),
                            "string_value": self.faker.pystr(min_chars=1, max_chars=256),
                        }
                    },
                    "message_deduplication_id": self.faker.pystr(min_chars=1, max_chars=128),
                    "message_group_id": self.faker.pystr(min_chars=1, max_chars=128),
                },
                {
                    "id": self.faker.pystr(min_chars=1, max_chars=100),
                    "message": self.faker.pystr(min_chars=1, max_chars=256),
                    "subject": self.faker.pystr(min_chars=1, max_chars=256),
                    "message_attributes": {
                        self.faker.pystr(min_chars=1, max_chars=20): {
                            "data_type": self.faker.random_element(MessageAttributeDataTypes),
                            "string_value": self.faker.pystr(min_chars=1, max_chars=256),
                        }
                    },
                    "message_deduplication_id": self.faker.pystr(min_chars=1, max_chars=128),
                    "message_group_id": self.faker.pystr(min_chars=1, max_chars=128),
                },
            ],
        }
        expected_response = {
            "Successful": [
                {
                    "Id": message_data["publish_batch_request_entries"][0]["id"],
                    "MessageId": self.faker.pystr(min_chars=1, max_chars=256),
                    "SequenceNumber": self.faker.pystr(min_chars=1, max_chars=100),
                },
            ],
            "Failed": [
                {
                    "Id": message_data["publish_batch_request_entries"][1]["id"],
                    "MessageId": self.faker.pystr(min_chars=1, max_chars=256),
                    "SequenceNumber": self.faker.pystr(min_chars=1, max_chars=100),
                },
            ],
        }
        with mock.patch.object(
            self.publish.client, "publish_batch", return_value=expected_response
        ):
            response = self.publish.publish_batch(message_data)
            self.assertEqual(response, expected_response)
            self.assertEqual(
                response["Failed"][0]["Id"],
                message_data["publish_batch_request_entries"][1]["id"],
            )

    def test_publish_batch_client_error(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        message_data = {
            "topic_arn": generate_random_arn(self.faker, name),
            "publish_batch_request_entries": [
                {
                    "id": self.faker.pystr(min_chars=1, max_chars=100),
                    "message": self.faker.pystr(min_chars=1, max_chars=256),
                    "subject": self.faker.pystr(min_chars=1, max_chars=256),
                    "message_attributes": {
                        self.faker.pystr(min_chars=1, max_chars=20): {
                            "data_type": self.faker.random_element(MessageAttributeDataTypes),
                            "string_value": self.faker.pystr(min_chars=1, max_chars=256),
                        }
                    },
                    "message_deduplication_id": self.faker.pystr(min_chars=1, max_chars=128),
                    "message_group_id": self.faker.pystr(min_chars=1, max_chars=128),
                },
            ],
        }
        expected_error = Mock(side_effect=ClientError({}, "publish_batch"))
        expected_response = (
            "An error occurred (Unknown) when calling the publish_batch operation: Unknown"
        )
        with mock.patch.object(self.publish.client, "publish_batch", expected_error):
            with self.assertRaises(NotificationError):
                response = self.publish.publish_batch(message_data)
                self.assertEqual(response, expected_response)

    def test_publish_batch_validation_error(self):
        name = self.faker.pystr(min_chars=260, max_chars=300)
        message_data = {
            "topic_arn": generate_random_arn(self.faker, name),
            "publish_batch_request_entries": [
                {
                    "id": self.faker.pystr(min_chars=1, max_chars=100),
                    "message": self.faker.pystr(min_chars=1, max_chars=256),
                    "subject": self.faker.pystr(min_chars=1, max_chars=256),
                    "message_attributes": {
                        self.faker.pystr(min_chars=1, max_chars=20): {
                            "data_type": self.faker.random_element(MessageAttributeDataTypes),
                            "string_value": self.faker.pystr(min_chars=1, max_chars=256),
                        }
                    },
                    "message_deduplication_id": self.faker.pystr(min_chars=1, max_chars=128),
                    "message_group_id": self.faker.pystr(min_chars=1, max_chars=128),
                },
            ],
        }
        expected_response = f"Validation error in Field 'topic_arn' - Value should have at most 256 items after validation, not {len(message_data['topic_arn'])}"
        with mock.patch.object(self.publish.client, "publish_batch"):
            with self.assertRaises(NotificationError):
                response = self.publish.publish_batch(message_data)
                self.assertEqual(response, expected_response)
