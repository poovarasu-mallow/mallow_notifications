import unittest
from typing import Optional
from unittest import mock
from unittest.mock import MagicMock, Mock, patch

from botocore.exceptions import ClientError
from faker import Faker
from pydantic_core import ValidationError

from mallow_notifications.base.logger import get_logger
from mallow_notifications.base.utils import generate_random_arn
from mallow_notifications.sns import SNSTopics
from mallow_notifications.sns.endpoints.topics import NotificationError
from mallow_notifications.sns.schema.topics import CreateTopicRequest

faker = Faker()
logging = get_logger(__name__)


class BaseTopic(unittest.TestCase):
    def setUp(self):
        self.topics = SNSTopics()
        self.mock_client = MagicMock()
        self.topics.client = self.mock_client
        self.faker = Faker()


class TestCreateTopic(BaseTopic):
    def test_create_topic_success_response(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        topic_data = {"topic_name": name}
        expected_response = {"TopicArn": generate_random_arn(self.faker, name)}
        with mock.patch.object(self.topics.client, "create_topic", return_value=expected_response):
            response = self.topics.create_topic(topic_data)
            self.assertEqual(response, expected_response)

    def test_create_topic_success_with_all_fields(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        topic_data = {
            "topic_name": name,
            "topic_attributes": {
                "DisplayName": self.faker.name(),
            },
            "topic_tags": [
                {
                    "key": self.faker.pystr(min_chars=1, max_chars=256),
                    "value": self.faker.pystr(min_chars=1, max_chars=256),
                }
            ],
            "topic_data_protection_policy": self.faker.pystr(min_chars=1, max_chars=256),
        }
        expected_response = {"TopicArn": generate_random_arn(self.faker, name)}
        with mock.patch.object(self.topics.client, "create_topic", return_value=expected_response):
            response = self.topics.create_topic(topic_data)
            self.assertEqual(response, expected_response)

    def test_create_topic_error_response(self):
        name = self.faker.pystr(min_chars=1, max_chars=256)
        topic_data = {"topic_name": name}
        expected_response = {"TopicArn": generate_random_arn(self.faker, name)}
        with mock.patch.object(
            self.topics.client,
            "create_topic",
            return_value={"TopicArn": generate_random_arn(self.faker, name)},
        ):
            response = self.topics.create_topic(topic_data)
            self.assertNotEqual(response, expected_response)

    def test_create_topic_client_error(self):
        name = self.faker.pystr(min_chars=1, max_chars=256)
        topic_data = {"topic_name": name}
        expected_error = Mock(side_effect=ClientError({}, "create_topic"))
        expected_response = (
            "An error occurred (Unknown) when calling the create_topic operation: Unknown"
        )
        with mock.patch.object(self.topics.client, "create_topic", expected_error):
            with self.assertRaises(NotificationError):
                response = self.topics.create_topic(topic_data)
                self.assertEqual(response, expected_response)

    def test_create_topic_validation_error(self):
        topic_data = {"topic_name": ""}
        with mock.patch.object(self.topics.client, "create_topic"):
            with self.assertRaises(NotificationError):
                response = self.topics.create_topic(topic_data)
                self.assertEqual(
                    response,
                    "Validation error in Field 'topic_name' - String should have at least 1 character",
                )

    def test_create_topic_sns_error(self):
        name = self.faker.pystr(min_chars=1, max_chars=256)
        topic_data = {"topic_name1": name}
        expected_error = Mock(
            side_effect=self.topics.client.exceptions.InvalidParameterException({}, "create_topic")
        )
        with mock.patch.object(self.topics.client, "create_topic", expected_error):
            with self.assertRaises(NotificationError):
                self.topics.create_topic(topic_data)


class TestListTopics(BaseTopic):
    def test_list_topics_success(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        expected_response = {"Topics": [{"TopicArn": generate_random_arn(self.faker, name)}]}
        with mock.patch.object(self.topics.client, "list_topics", return_value=expected_response):
            response = self.topics.list_topics()
            self.assertEqual(response, expected_response)

    def test_list_topics_success_with_valid_next_token(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        next_token = {"NextToken": str(self.faker.random_int(min=1, max=10))}
        expected_response = {"Topics": [{"TopicArn": generate_random_arn(self.faker, name)}]}
        with mock.patch.object(self.topics.client, "list_topics", return_value=expected_response):
            response = self.topics.list_topics(next_token)
            self.assertEqual(response, expected_response)

    def test_list_topics_success_with_invalid_next_token(self):
        name = self.faker.pystr(min_chars=1, max_chars=256)
        next_token = {"NextToken": self.faker.random_int(min=1, max=10)}
        expected_response = (
            "Validation error in Field 'NextToken' - Input should be a valid string"
        )
        with mock.patch.object(self.topics.client, "create_topic"):
            with self.assertRaises(NotificationError):
                response = self.topics.list_topics(next_token)
                self.assertEqual(response, expected_response)

    def test_create_topic_client_error(self):
        expected_error = Mock(side_effect=ClientError({}, "list_topics"))
        expected_response = (
            "An error occurred (Unknown) when calling the list_topics operation: Unknown"
        )
        with mock.patch.object(self.topics.client, "list_topics", expected_error):
            with self.assertRaises(NotificationError):
                response = self.topics.list_topics()
                self.assertEqual(response, expected_response)


class TestSetTopicAttributes(BaseTopic):
    def test_set_topic_attributes_success(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        topic_attributes = {
            "topic_arn": generate_random_arn(self.faker, name),
            "attribute_name": "DisplayName",
            "attribute_value": self.faker.name(),
        }
        with mock.patch.object(self.topics.client, "set_topic_attributes", return_value=None):
            response = self.topics.set_topic_attributes(topic_attributes)
            self.assertIsNone(response)

    def test_set_topic_attributes_client_error(self):
        name = self.faker.pystr(min_chars=1, max_chars=256)
        topic_attributes = {
            "topic_arn": generate_random_arn(self.faker, name),
            "attribute_name": "DisplayName",
            "attribute_value": self.faker.name(),
        }
        expected_error = Mock(side_effect=ClientError({}, "set_topic_attributes"))
        expected_response = (
            "An error occurred (Unknown) when calling the set_topic_attributes operation: Unknown"
        )
        with mock.patch.object(self.topics.client, "set_topic_attributes", expected_error):
            with self.assertRaises(NotificationError):
                response = self.topics.set_topic_attributes(topic_attributes)
                self.assertEqual(response, expected_response)

    def test_set_topic_attributes_validation_error(self):
        topic_arn = generate_random_arn(self.faker, self.faker.pystr(min_chars=250, max_chars=300))
        topic_attributes = {
            "topic_arn": topic_arn,
            "attribute_name": self.faker.pystr(min_chars=1, max_chars=256),
            "attribute_value": self.faker.pystr(min_chars=1, max_chars=256),
        }
        expected_response = f"Validation error in Field 'topic_arn' - Value should have at most 256 items after validation, not {len(topic_arn)}"
        with mock.patch.object(self.topics.client, "set_topic_attributes"):
            with self.assertRaises(NotificationError):
                response = self.topics.set_topic_attributes(topic_attributes)
                self.assertEqual(response, expected_response)


class TestGetTopicAttributes(BaseTopic):
    def test_get_topic_attributes_success(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        topic_arn = {"TopicArn": generate_random_arn(self.faker, name)}
        expected_response = {"Attributes": {"DisplayName": name}}
        with mock.patch.object(
            self.topics.client, "get_topic_attributes", return_value=expected_response
        ):
            response = self.topics.get_topic_attributes(topic_arn)
            self.assertEqual(response, expected_response)

    def test_get_topic_attributes_error_response(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        topic_arn = {"TopicArn": generate_random_arn(self.faker, name)}
        expected = {
            "Attributes": {
                "Policy": '{"Version":"2008Owner-10-17","Id":"__default_policy_ID","Statement":[{"Sid":"__default_statement_ID","Effect":"Allow","Principal":{"AWS":"*"},"Action":["SNS:GetTopicAttributes","SNS:SetTopicAttributes","SNS:AddPermission","SNS:RemovePermission","SNS:DeleteTopic","SNS:Subscribe","SNS:ListSubscriptionsByTopic","SNS:Publish"],"Resource": '
                + generate_random_arn(self.faker, name)
                + ',"Condition":{"StringEquals":{"AWS:SourceOwner": '
                + self.faker.pystr(min_chars=1, max_chars=100)
                + "}}}]}",
                "Owner": self.faker.pystr(min_chars=1, max_chars=100),
                "SubscriptionsPending": "0",
                "TopicArn": generate_random_arn(self.faker, name),
                "EffectiveDeliveryPolicy": '{"http":{"defaultHealthyRetryPolicy":{"minDelayTarget":20,"maxDelayTarget":20,"numRetries":3,"numMaxDelayRetries":0,"numNoDelayRetries":0,"numMinDelayRetries":0,"backoffFunction":"linear"},"disableSubscriptionOverrides":false,"defaultRequestPolicy":{"headerContentType":"text/plain; charset=UTF-8"}}}',
                "SubscriptionsConfirmed": self.faker.random_element(["0", "1"]),
                "DisplayName": self.faker.name(),
                "SubscriptionsDeleted": "0",
            },
        }
        expected_response = {"Attributes": {"DisplayName": name}}
        with mock.patch.object(self.topics.client, "get_topic_attributes", return_value=expected):
            response = self.topics.get_topic_attributes(topic_arn)
            self.assertNotEqual(response, expected_response)

    def test_get_topic_attributes_client_error(self):
        name = self.faker.pystr(min_chars=1, max_chars=256)
        topic_arn = {"TopicArn": generate_random_arn(self.faker, name)}
        expected_error = Mock(side_effect=ClientError({}, "get_topic_attributes"))
        expected_response = (
            "An error occurred (Unknown) when calling the get_topic_attributes operation: Unknown"
        )
        with mock.patch.object(self.topics.client, "get_topic_attributes", expected_error):
            with self.assertRaises(NotificationError):
                response = self.topics.get_topic_attributes(topic_arn)
                self.assertEqual(response, expected_response)

    def test_get_topic_attributes_validation_error(self):
        topic_arn = {
            "TopicArn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=270, max_chars=300)
            )
        }
        expected_response = f"Validation error in Field 'topic_arn' - Value should have at most 256 items after validation, not {len(topic_arn)}"
        with mock.patch.object(self.topics.client, "get_topic_attributes"):
            with self.assertRaises(NotificationError):
                response = self.topics.get_topic_attributes(topic_arn)
                self.assertEqual(response, expected_response)


class TestDeleteTopic(BaseTopic):
    def test_delete_topic_success(self):
        name = self.faker.pystr(min_chars=1, max_chars=180)
        topic_arn = {"TopicArn": generate_random_arn(self.faker, name)}
        expected_response = {}
        with mock.patch.object(self.topics.client, "delete_topic", return_value=None):
            response = self.topics.delete_topic(topic_arn)
            self.assertIsNone(response)

    def test_delete_topic_client_error(self):
        name = self.faker.pystr(min_chars=1, max_chars=256)
        topic_arn = {"TopicArn": generate_random_arn(self.faker, name)}
        expected_error = Mock(side_effect=ClientError({}, "delete_topic"))
        expected_response = (
            "An error occurred (Unknown) when calling the delete_topic operation: Unknown"
        )
        with mock.patch.object(self.topics.client, "delete_topic", expected_error):
            with self.assertRaises(NotificationError):
                response = self.topics.delete_topic(topic_arn)
                self.assertEqual(response, expected_response)

    def test_delete_topic_validation_error(self):
        topic_arn = {
            "TopicArn": generate_random_arn(
                self.faker, self.faker.pystr(min_chars=250, max_chars=300)
            )
        }
        expected_response = f"Validation error in Field 'topic_arn' - Value should have at most 256 items after validation, not {len(topic_arn)}"
        with mock.patch.object(self.topics.client, "delete_topic"):
            with self.assertRaises(NotificationError):
                response = self.topics.delete_topic(topic_arn)
                self.assertEqual(response, expected_response)
