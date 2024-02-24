import unittest
from typing import Optional
from unittest import mock
from unittest.mock import MagicMock, Mock, patch

from botocore.exceptions import ClientError
from faker import Faker
from pydantic_core import ValidationError

from mallow_notifications.base.logger import get_logger
from mallow_notifications.base.utils import generate_random_arn
from mallow_notifications.sns import SNSTopicSubscribe
from mallow_notifications.sns.endpoints.topics import NotificationError
from mallow_notifications.sns.schema.topics import CreateTopicRequest

faker = Faker()
logging = get_logger(__name__)


class BaseSubscribeTest(unittest.TestCase):
    def setUp(self):
        self.subscribe = SNSTopicSubscribe()
        self.mock_client = MagicMock()
        self.subscribe.client = self.mock_client
        self.faker = Faker()


class TestSubscribe(BaseSubscribeTest):
    def test_subscribe_success_response(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        subscription_data = {
            "topic_arn": name,
            "protocol": "email",
            "endpoint": self.faker.email(),
        }
        expected_response = {"SubscriptionArn": generate_random_arn(self.faker, name)}
        with mock.patch.object(self.subscribe.client, "subscribe", return_value=expected_response):
            response = self.subscribe.subscribe(subscription_data)
            self.assertEqual(response, expected_response)

    def test_subscribe_success_with_all_fields(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        subscription_data = {
            "topic_arn": name,
            "protocol": "email",
            "endpoint": self.faker.email(),
            "attributes": {
                "raw_message_delivery": self.faker.random_element([True, False]),
            },
            "data_protection_policy": self.faker.pystr(min_chars=1, max_chars=256),
        }
        expected_response = {"SubscriptionArn": generate_random_arn(self.faker, name)}
        with mock.patch.object(self.subscribe.client, "subscribe", return_value=expected_response):
            response = self.subscribe.subscribe(subscription_data)
            self.assertEqual(response, expected_response)

    def test_subscribe_invalid_input(self):
        name = self.faker.pystr(min_chars=1, max_chars=256)
        subscription_data = {"topic_arn": name, "protocol": "email"}
        with self.assertRaises(NotificationError):
            self.subscribe.subscribe(subscription_data)

    def test_subscribe_client_error(self):
        name = self.faker.pystr(min_chars=1, max_chars=256)
        subscription_data = {
            "topic_arn": name,
            "protocol": "email",
            "endpoint": self.faker.email(),
        }
        expected_error = Mock(side_effect=ClientError({}, "subscribe"))
        expected_response = (
            "An error occurred (Unknown) when calling the get_topic_attributes operation: Unknown"
        )
        with mock.patch.object(self.subscribe.client, "subscribe", expected_error):
            with self.assertRaises(NotificationError):
                response = self.subscribe.subscribe(subscription_data)
                self.assertEqual(response, expected_response)

    def test_subscribe_validation_error(self):
        subscription_data = {"topic_arn": self.faker.pystr(min_chars=250, max_chars=300)}
        expected_response = f"Validation error in Field 'subscription_data' - Value should have at most 256 items after validation, not {len(subscription_data)}"
        with mock.patch.object(self.subscribe.client, "subscribe"):
            with self.assertRaises(NotificationError):
                response = self.subscribe.subscribe(subscription_data)
                self.assertEqual(response, expected_response)


class TestConfirmSubscribe(BaseSubscribeTest):
    def test_confirm_subscribe_success_response(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        subscription_data = {
            "topic_arn": generate_random_arn(self.faker, name),
            "token": self.faker.pystr(min_chars=1, max_chars=256),
            "authenticate_on_unsubscribe": self.faker.random_element(["true", "false"]),
        }
        expected_response = {"SubscriptionArn": generate_random_arn(self.faker, name)}
        with mock.patch.object(
            self.subscribe.client,
            "confirm_subscription",
            return_value=expected_response,
        ):
            response = self.subscribe.confirm_subscribe(subscription_data)
            self.assertEqual(response, expected_response)

    def test_confirm_subscribe_invalid_token(self):
        name = self.faker.pystr(min_chars=1, max_chars=256)
        subscription_data = {
            "topic_arn": generate_random_arn(self.faker, name),
            "token": None,
            "authenticate_on_unsubscribe": self.faker.random_element(["true", "false"]),
        }
        with self.assertRaises(NotificationError):
            self.subscribe.confirm_subscribe(subscription_data)

    def test_confirm_subscribe_client_error(self):
        name = self.faker.pystr(min_chars=1, max_chars=256)
        subscription_data = {
            "topic_arn": generate_random_arn(self.faker, name),
            "token": self.faker.pystr(min_chars=1, max_chars=256),
            "authenticate_on_unsubscribe": self.faker.random_element(["true", "false"]),
        }
        expected_response = (
            "An error occurred (Unknown) when calling the get_topic_attributes operation: Unknown"
        )
        expected_error = Mock(side_effect=ClientError({}, "confirm_subscription"))
        with mock.patch.object(self.subscribe.client, "confirm_subscription", expected_error):
            with self.assertRaises(NotificationError):
                response = self.subscribe.confirm_subscribe(subscription_data)
                self.assertEqual(response, expected_response)

    def test_confirm_subscribe_validation_error(self):
        subscription_data = {
            "topic_arn": self.faker.pystr(min_chars=260, max_chars=300),
            "token": self.faker.pystr(min_chars=1, max_chars=256),
            "authenticate_on_unsubscribe": self.faker.random_element(["true", "false"]),
        }
        expected_response = f"Validation error in Field 'subscription_data' - Value should have at most 256 items after validation, not {len(subscription_data)}"
        with mock.patch.object(self.subscribe.client, "confirm_subscription"):
            with self.assertRaises(NotificationError):
                response = self.subscribe.confirm_subscribe(subscription_data)
                self.assertEqual(response, expected_response)


class TestUnSubscribe(BaseSubscribeTest):
    def test_unsubscribe_success_response(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        subscription_data = {
            "subscription_arn": generate_random_arn(self.faker, name),
        }
        with mock.patch.object(self.subscribe.client, "unsubscribe", return_value=None):
            response = self.subscribe.unsubscribe(subscription_data)
            self.assertIsNone(response)

    def test_unsubscribe_client_error(self):
        name = self.faker.pystr(min_chars=1, max_chars=256)
        subscription_data = {
            "subscription_arn": generate_random_arn(self.faker, name),
        }
        expected_error = Mock(side_effect=ClientError({}, "unsubscribe"))
        expected_response = (
            "An error occurred (Unknown) when calling the get_topic_attributes operation: Unknown"
        )
        with mock.patch.object(self.subscribe.client, "unsubscribe", expected_error):
            with self.assertRaises(NotificationError):
                response = self.subscribe.unsubscribe(subscription_data)
                self.assertEqual(response, expected_response)

    def test_unsubscribe_validation_error(self):
        subscription_data = {
            "subscription_arn": self.faker.pystr(min_chars=260, max_chars=300),
        }
        expected_response = f"Validation error in Field 'subscription_data' - Value should have at most 256 items after validation, not {len(subscription_data)}"
        with mock.patch.object(self.subscribe.client, "unsubscribe"):
            with self.assertRaises(NotificationError):
                response = self.subscribe.unsubscribe(subscription_data)
                self.assertEqual(response, expected_response)


class ListSubscriptions(BaseSubscribeTest):
    def test_list_subscriptions_success_response(self):
        expected_response = {
            "Subscriptions": [
                {
                    "SubscriptionArn": generate_random_arn(
                        self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                    ),
                    "Owner": self.faker.pystr(min_chars=1, max_chars=100),
                    "Protocol": "email",
                    "Endpoint": self.faker.email(),
                    "TopicArn": generate_random_arn(
                        self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                    ),
                }
            ]
        }
        with mock.patch.object(
            self.subscribe.client, "list_subscriptions", return_value=expected_response
        ):
            response = self.subscribe.list_subscriptions()
            self.assertEqual(response, expected_response)

    def test_list_subscriptions_success_response_with_next_token(self):
        next_token = {"NextToken": self.faker.pystr(min_chars=1, max_chars=256)}
        expected_response = {"Subscriptions": []}
        with mock.patch.object(
            self.subscribe.client, "list_subscriptions", return_value=expected_response
        ):
            response = self.subscribe.list_subscriptions(next_token)
            self.assertEqual(response, expected_response)

    def test_list_subscriptions_client_error(self):
        expected_error = Mock(side_effect=ClientError({}, "list_subscriptions"))
        expected_response = (
            "An error occurred (Unknown) when calling the get_topic_attributes operation: Unknown"
        )
        with mock.patch.object(self.subscribe.client, "list_subscriptions", expected_error):
            with self.assertRaises(NotificationError):
                response = self.subscribe.list_subscriptions()
                self.assertEqual(response, expected_response)

    def test_list_subscriptions_invalid_next_token(self):
        next_token = {"NextToken": self.faker.random_int(min=1, max=10)}
        expected_response = (
            "Validation error in Field 'NextToken' - Input should be a valid string"
        )
        with mock.patch.object(self.subscribe.client, "list_subscriptions"):
            with self.assertRaises(NotificationError):
                response = self.subscribe.list_subscriptions(next_token)
                self.assertEqual(response, expected_response)


class TestSubscribeTopics(BaseSubscribeTest):
    def test_subscribe_topics_success_response(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        subscription_data = {
            "topic_arn": generate_random_arn(self.faker, name),
        }
        expected_response = {
            "Subscriptions": [
                {
                    "SubscriptionArn": generate_random_arn(
                        self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                    ),
                    "Owner": self.faker.pystr(min_chars=1, max_chars=100),
                    "Protocol": "email",
                    "Endpoint": self.faker.email(),
                    "TopicArn": generate_random_arn(
                        self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                    ),
                }
            ]
        }
        with mock.patch.object(
            self.subscribe.client,
            "list_subscriptions_by_topic",
            return_value=expected_response,
        ):
            response = self.subscribe.list_subscriptions_by_topic(subscription_data)
            self.assertEqual(response, expected_response)

    def test_subscribe_topics_with_next_token(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        subscription_data = {
            "topic_arn": generate_random_arn(self.faker, name),
            "next_token": self.faker.pystr(min_chars=1, max_chars=100),
        }
        expected_response = {"Subscriptions": []}
        with mock.patch.object(
            self.subscribe.client,
            "list_subscriptions_by_topic",
            return_value=expected_response,
        ):
            response = self.subscribe.list_subscriptions_by_topic(subscription_data)
            self.assertEqual(response, expected_response)

    def test_subscribe_topic_with_invalid_topic(self):
        subscription_data = {
            "topic_arn": self.faker.pystr(min_chars=260, max_chars=300),
        }
        expected_response = f"Validation error in Field 'topic_arn' - Value should have at most 256 items after validation, not {len(subscription_data)}"
        with mock.patch.object(self.subscribe.client, "list_subscriptions_by_topic"):
            with self.assertRaises(NotificationError):
                response = self.subscribe.list_subscriptions_by_topic(subscription_data)
                self.assertEqual(response, expected_response)

    def test_subscribe_topic_with_invalid_next_token(self):
        subscription_data = {
            "topic_arn": self.faker.pystr(min_chars=1, max_chars=180),
            "next_token": self.faker.random_int(min=1, max=10),
        }
        expected_response = (
            "Validation error in Field 'next_token' - Input should be a valid string"
        )
        with mock.patch.object(self.subscribe.client, "list_subscriptions_by_topic"):
            with self.assertRaises(NotificationError):
                response = self.subscribe.list_subscriptions_by_topic(subscription_data)
                self.assertEqual(response, expected_response)

    def test_subscribe_topic_client_error(self):
        subscription_data = {
            "topic_arn": self.faker.pystr(min_chars=1, max_chars=180),
        }
        expected_error = Mock(side_effect=ClientError({}, "list_subscriptions_by_topic"))
        expected_response = "An error occurred (Unknown) when calling the list_subscriptions_by_topic operation: Unknown"
        with mock.patch.object(
            self.subscribe.client, "list_subscriptions_by_topic", expected_error
        ):
            with self.assertRaises(NotificationError):
                response = self.subscribe.list_subscriptions_by_topic(subscription_data)
                self.assertEqual(response, expected_response)


class TestGetSubscribtionAttributes(BaseSubscribeTest):
    def test_get_subscription_attributes_success_response(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        subscription_data = {
            "subscription_arn": generate_random_arn(self.faker, name),
        }
        expected_response = {
            "Attributes": {
                "TopicArn": generate_random_arn(
                    self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                ),
            }
        }
        with mock.patch.object(
            self.subscribe.client,
            "get_subscription_attributes",
            return_value=expected_response,
        ):
            response = self.subscribe.get_subscription_attributes(subscription_data)
            self.assertEqual(response, expected_response)

    def test_get_subscription_attributes_client_error(self):
        subscription_data = {
            "subscription_arn": self.faker.pystr(min_chars=1, max_chars=180),
        }
        expected_error = Mock(side_effect=ClientError({}, "get_subscription_attributes"))
        expected_response = "An error occurred (Unknown) when calling the get_subscription_attributes operation: Unknown"
        with mock.patch.object(
            self.subscribe.client, "get_subscription_attributes", expected_error
        ):
            with self.assertRaises(NotificationError):
                response = self.subscribe.get_subscription_attributes(subscription_data)
                self.assertEqual(response, expected_response)

    def test_get_subscription_attributes_with_invalid_subscription_arn(self):
        subscription_data = {
            "subscription_arn": self.faker.pystr(min_chars=260, max_chars=300),
        }
        expected_response = f"Validation error in Field 'subscription_arn' - Value should have at most 256 items after validation, not {len(subscription_data)}"
        with mock.patch.object(self.subscribe.client, "get_subscription_attributes"):
            with self.assertRaises(NotificationError):
                response = self.subscribe.get_subscription_attributes(subscription_data)
                self.assertEqual(response, expected_response)


class TestSetSubscriptionAttributes(BaseSubscribeTest):
    def test_set_subscription_attributes_success_response(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        subscription_data = {
            "subscription_arn": generate_random_arn(self.faker, name),
            "attribute_name": self.faker.pystr(min_chars=1, max_chars=256),
            "attribute_value": self.faker.pystr(min_chars=1, max_chars=256),
        }
        expected_response = {}
        with mock.patch.object(
            self.subscribe.client,
            "set_subscription_attributes",
            return_value=expected_response,
        ):
            response = self.subscribe.set_subscription_attributes(subscription_data)
            self.assertEqual(response, expected_response)

    def test_set_subscription_attributes_client_error(self):
        subscription_data = {
            "subscription_arn": self.faker.pystr(min_chars=1, max_chars=180),
            "attribute_name": self.faker.pystr(min_chars=1, max_chars=256),
            "attribute_value": self.faker.pystr(min_chars=1, max_chars=256),
        }
        expected_error = Mock(side_effect=ClientError({}, "set_subscription_attributes"))
        expected_response = "An error occurred (Unknown) when calling the set_subscription_attributes operation: Unknown"
        with mock.patch.object(
            self.subscribe.client, "set_subscription_attributes", expected_error
        ):
            with self.assertRaises(NotificationError):
                response = self.subscribe.set_subscription_attributes(subscription_data)
                self.assertEqual(response, expected_response)

    def test_set_subscription_attributes_with_invalid_subscription_arn(self):
        subscription_data = {
            "subscription_arn": self.faker.pystr(min_chars=260, max_chars=300),
            "attribute_name": self.faker.pystr(min_chars=1, max_chars=256),
            "attribute_value": self.faker.pystr(min_chars=1, max_chars=256),
        }
        expected_response = f"Validation error in Field 'subscription_arn' - Value should have at most 256 items after validation, not {len(subscription_data)}"
        with mock.patch.object(self.subscribe.client, "set_subscription_attributes"):
            with self.assertRaises(NotificationError):
                response = self.subscribe.set_subscription_attributes(subscription_data)
                self.assertEqual(response, expected_response)
