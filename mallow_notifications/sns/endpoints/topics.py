"""This module contains the `SNSTopics` class for sending SNS messages.

This module provides functionality for sending SNS messages using the
boto3 AWS SDK for Python.
"""

from typing import Dict, Optional, Union

from botocore.exceptions import ClientError
from pydantic import ValidationError

from mallow_notifications.base.exceptions import NotificationError
from mallow_notifications.base.logger import get_logger
from mallow_notifications.base.utils import NotificationError, handle_validation_error
from mallow_notifications.sns.endpoints import SNSClient
from mallow_notifications.sns.schema.base import NextToken
from mallow_notifications.sns.schema.topics import (
    CreateTopicRequest,
    GetTopicAttributesResponse,
    ListTopicsResponse,
    SetTopicAttributesRequest,
    TopicArnResoponse,
    TopicArnSchema,
)

logging = get_logger(__name__)


class SNSTopics(SNSClient):
    """Class for sending SNS messages using the boto3 AWS SDK for Python."""

    def __init__(self):
        super().__init__()

    # pylint: disable=line-too-long
    def create_topic(
        self, topic_data: Union[CreateTopicRequest, Dict[str, any]]
    ) -> TopicArnResoponse:
        """Creates an Amazon SNS topic.

        Parameters:
        - name (str): [REQUIRED] The name of the topic you want to create.
          Constraints: Topic names must be made up of only uppercase and lowercase ASCII letters,
          numbers, underscores, and hyphens, and must be between 1 and 256 characters long.
          For a FIFO (first-in-first-out) topic, the name must end with the .fifo suffix.

        - attributes (dict): A map of attributes with their corresponding values.
          - DeliveryPolicy (str): The policy that defines how Amazon SNS retries failed deliveries to HTTP/S endpoints.
          - DisplayName (str): The display name to use for a topic with SMS subscriptions.
          - FifoTopic (bool): Set to true to create a FIFO topic.
          - Policy (str): The policy that defines who can access your topic.
          - SignatureVersion (str): The signature version corresponds to the hashing algorithm used while creating
            the signature of the notifications, subscription confirmations, or unsubscribe confirmation messages sent by Amazon notifications.sns.
          - TracingConfig (dict): Tracing mode of an Amazon SNS topic.
            - Enabled (bool): Set to true to enable tracing.
            - IncludeFirehose (bool): When set to true, AWS X-Ray tracing is enabled. If IncludeFirehose is set to true,
              Amazon SNS sends trace data to Amazon Kinesis Data Firehose.
            - IncludeExternalId (bool): Set IncludeExternalId to true to include the ExternalId in the trace data.
            - IncludeLogRoot (bool): Set IncludeLogRoot to true to include the log file name and line number in the trace data.
            - IncludeOrganization (bool): Set to true to include trace data from the organization.
            - UseExistingActiveTraceHeader (bool): Set to true to use existing active trace headers as they are.
            - Sampled (bool): Set to true to sample the trace data.
          - KmsMasterKeyId (str): The ID of an Amazon Web Services managed customer master key (CMK) for Amazon SNS or a custom CMK.

        - tags (list): The list of tags to add to a new topic.
          - (dict) Tag: The list of tags to be added to the specified topic.
            - Key (str) [REQUIRED]: The required key portion of the tag.
            - Value (str) [REQUIRED]: The optional value portion of the tag.

        - data_protection_policy (str): The body of the policy document you want to use for this topic.
          You can only add one policy per topic.
          The policy must be in JSON string format.
          Length Constraints: Maximum length of 30,720.

        Returns:
        - topic_arn (str): The Amazon Resource Name (ARN) of the created topic along with the response metadata.

        Raises:
        - Exception: If there is an error during topic creation.
        """
        try:
            data = CreateTopicRequest.process_input(topic_data)
            response = self.client.create_topic(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.TopicLimitExceededException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InvalidSecurityException,
            self.client.exceptions.TagLimitExceededException,
            self.client.exceptions.StaleTagException,
            self.client.exceptions.ConcurrentAccessException,
        ) as e:
            raise NotificationError(e)

    # pylint: disable=dangerous-default-value
    def list_topics(
        self, next_token: Optional[Union[NextToken, Dict[str, str]]] = {"NextToken": None}
    ) -> ListTopicsResponse:
        """Returns a list of the requester's topics. Each call returns a
        limited list of topics, up to 100. If there are more topics, a
        NextToken is also returned. Use the NextToken parameter in a new
        ListTopics call to get further results.

        This action is throttled at 30 transactions per second (TPS).
        """
        try:
            data = NextToken.process_input(next_token)
            response = self.client.list_topics(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.AuthorizationErrorException,
        ) as e:
            raise NotificationError(e)

    def set_topic_attributes(
        self, topic_attributes: Union[SetTopicAttributesRequest, Dict[str, any]]
    ):
        """Allows a topic owner to set an attribute of the topic to a new
        value."""
        try:
            data = SetTopicAttributesRequest.process_input(topic_attributes)
            response = self.client.set_topic_attributes(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.NotFoundException,
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InvalidSecurityException,
        ) as e:
            raise NotificationError(e)

    def get_topic_attributes(
        self, topic_arn: Union[TopicArnSchema, Dict[str, str]]
    ) -> GetTopicAttributesResponse:
        """Returns all of the properties of a topic.

        Topic properties returned might differ based on the
        authorization of the user.
        """
        try:
            data = TopicArnSchema.process_input(topic_arn)
            response = self.client.get_topic_attributes(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.NotFoundException,
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InvalidSecurityException,
        ) as e:
            raise NotificationError(e)

    def delete_topic(self, topic_arn: Union[TopicArnSchema, Dict[str, str]]):
        """Deletes a topic and all its subscriptions.

        Deleting a topic might prevent some messages previously sent to
        the topic from being delivered to subscribers. This action is
        idempotent, so deleting a topic that does not exist does not
        result in an error.
        """
        try:
            data = TopicArnSchema.process_input(topic_arn)
            response = self.client.delete_topic(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.InvalidStateException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.NotFoundException,
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InvalidSecurityException,
            self.client.exceptions.StaleTagException,
            self.client.exceptions.TagPolicyException,
            self.client.exceptions.ConcurrentAccessException,
        ) as e:
            raise NotificationError(e)
