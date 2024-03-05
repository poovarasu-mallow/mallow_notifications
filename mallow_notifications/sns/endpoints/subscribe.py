"""This module contains the `SNSTopicSubscribe` class for sending SNS messages.

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
from mallow_notifications.sns.schema.subscribe import (
    ConfirmSubscriptionRequest,
    ListSubscriptionsResponse,
    ListSubscriptionTopicRequest,
    SetSubcribtionAttributesRequest,
    SubscribeAttributesResponse,
    SubscribeRequest,
    SubscribeResponse,
    SubscriptionArnSchema,
)

logger = get_logger(__name__)


class SNSTopicSubscribe(SNSClient):
    """Class for sending SNS messages using the boto3 AWS SDK for Python."""

    def __init__(self):
        super().__init__()

    def subscribe(
        self, subscription_data: Union[SubscribeRequest, Dict[str, any]]
    ) -> SubscribeResponse:
        """Subscribes an endpoint to an Amazon SNS topic. If the endpoint type
        is HTTP/S or email, or if the endpoint and the topic are not in the
        same Amazon Web Services account, the endpoint owner must run the
        ConfirmSubscription action to confirm the subscription.

        You call the ConfirmSubscription action with the token from the
        subscription response. Confirmation tokens are valid for two
        days.

        This action is throttled at 100 transactions per second (TPS).
        """
        try:
            data = SubscribeRequest.process_input(subscription_data)
            response = self.client.subscribe(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.SubscriptionLimitExceededException,
            self.client.exceptions.FilterPolicyLimitExceededException,
            self.client.exceptions.ReplayLimitExceededException,
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.NotFoundException,
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.InvalidSecurityException,
        ) as e:
            raise NotificationError(e)

    def confirm_subscribe(
        self, confirm_subscription_data: Union[ConfirmSubscriptionRequest, Dict[str, any]]
    ) -> SubscribeResponse:
        """Verifies an endpoint owner's intent to receive messages by
        validating the token sent to the endpoint by an earlier Subscribe
        action.

        If the token is valid, the action creates a new subscription and
        returns its Amazon Resource Name (ARN). This call requires an
        AWS signature only when the AuthenticateOnUnsubscribe flag is
        set to “true”.
        """
        try:
            data = ConfirmSubscriptionRequest.process_input(confirm_subscription_data)
            response = self.client.confirm_subscription(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.SubscriptionLimitExceededException,
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.NotFoundException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.FilterPolicyLimitExceededException,
            self.client.exceptions.ReplayLimitExceededException,
        ) as e:
            raise NotificationError(e)

    def unsubscribe(self, subscription_arn: Union[SubscriptionArnSchema, Dict[str, str]]) -> None:
        """Deletes a subscription.

        If the subscription requires authentication for deletion, only
        the owner of the subscription or the topic's owner can
        unsubscribe, and an Amazon Web Services signature is required.
        If the Unsubscribe call does not require authentication and the
        requester is not the subscription owner, a final cancellation
        message is delivered to the endpoint, so that the endpoint owner
        can easily resubscribe to the topic if the Unsubscribe request
        was unintended.
        """
        try:
            data = SubscriptionArnSchema.process_input(subscription_arn)
            response = self.client.unsubscribe(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.AuthorizationErrorException,
            self.client.exceptions.NotFoundException,
            self.client.exceptions.InvalidSecurityException,
        ) as e:
            raise NotificationError(e)

    # pylint: disable=dangerous-default-value
    def list_subscriptions(
        self, next_token: Optional[Union[NextToken, Dict[str, str]]] = {"NextToken": None}
    ) -> ListSubscriptionsResponse:
        """Returns a list of the requester's subscriptions. Each call returns a
        limited list of subscriptions, up to 100. If there are more
        subscriptions, a NextToken is also returned. Use the NextToken
        parameter in a new ListSubscriptions call to get further results.

        This action is throttled at 30 transactions per second (TPS).
        """
        try:
            data = NextToken.process_input(next_token)
            response = self.client.list_subscriptions(**data)
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

    def list_subscriptions_by_topic(
        self, list_topic_attributed: Union[ListSubscriptionTopicRequest, Dict[str, any]]
    ) -> ListSubscriptionsResponse:
        """Returns a list of the subscriptions to a specific topic. Each call
        returns a limited list of subscriptions, up to 100. If there are more
        subscriptions, a NextToken is also returned. Use the NextToken
        parameter in a new ListSubscriptionsByTopic call to get further
        results.

        This action is throttled at 30 transactions per second (TPS).
        """
        try:
            data = ListSubscriptionTopicRequest.process_input(list_topic_attributed)
            response = self.client.list_subscriptions_by_topic(**data)
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
        ) as e:
            raise NotificationError(e)

    def get_subscription_attributes(
        self, subsribtion_arn: Union[SubscriptionArnSchema, Dict[str, str]]
    ) -> SubscribeAttributesResponse:
        """Returns all of the properties of a subscription."""
        try:
            data = SubscriptionArnSchema.process_input(subsribtion_arn)
            response = self.client.get_subscription_attributes(**data)
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
        ) as e:
            raise NotificationError(e)

    def set_subscription_attributes(
        self, subscription_attributes: Union[SetSubcribtionAttributesRequest, Dict[str, any]]
    ) -> None:
        """Allows a subscription owner to set an attribute of the subscription
        to a new value."""
        try:
            data = SetSubcribtionAttributesRequest.process_input(subscription_attributes)
            response = self.client.set_subscription_attributes(**data)
            return response
        except ValidationError as e:
            handle_validation_error(e)
        except ClientError as e:
            raise NotificationError(e)
        except (
            self.client.exceptions.InvalidParameterException,
            self.client.exceptions.FilterPolicyLimitExceededException,
            self.client.exceptions.ReplayLimitExceededException,
            self.client.exceptions.InternalErrorException,
            self.client.exceptions.NotFoundException,
            self.client.exceptions.AuthorizationErrorException,
        ) as e:
            raise NotificationError(e)
