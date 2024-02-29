from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator

from mallow_notifications.base.constants import (
    FilterPolicyScopeEnum,
    ProtocolEnum,
    ReplayStatusEnum,
)
from mallow_notifications.sns.schema.base import BaseSchema, NextToken
from mallow_notifications.sns.schema.topics import TopicArnSchema


class SubscriptionArnSchema(BaseSchema):
    SubscriptionArn: str = Field(
        alias="subscription_arn", min_length=1, max_length=256, description="Subscription ARN"
    )


class SubscribeAttributes(BaseModel):
    DeliveryPolicy: Optional[Dict] = Field(
        default=None,
        alias="delivery_policy",
        description="The policy that defines how Amazon SNS retries failed deliveries to HTTP/S endpoints.",
    )
    FilterPolicy: Optional[Dict] = Field(
        default=None,
        alias="filter_policy",
        description="The simple JSON object that lets your subscriber receive only a subset of messages",
    )
    FilterPolicyScope: Optional[Union[FilterPolicyScopeEnum, Dict]] = Field(
        default=None,
        alias="filter_policy_scope",
        description="The type of filtering that is applied to received messages.",
    )
    RawMessageDelivery: Optional[bool] = Field(
        default=None, alias="raw_message_delivery", description="Enables raw message delivery."
    )
    RedrivePolicy: Optional[str] = Field(
        default=None,
        alias="redrive_policy",
        description="When specified, sends undeliverable messages to the specified Amazon SQS dead-letter queue.",
    )
    SubscriptionRoleArn: Optional[str] = Field(
        default=None,
        alias="subscription_role_arn",
        description="The ARN of the IAM role for SNS to use to confirm subscription.",
    )
    ReplayPolicy: Optional[str] = Field(
        default=None,
        alias="replay_policy",
        description="The policy that defines how Amazon SNS retries failed deliveries to HTTP/S endpoints.",
    )
    ReplayStatus: Optional[ReplayStatusEnum] = Field(
        default=None,
        alias="replay_status",
        description="Indicates whether the subscription has active or passive opted-in subscriptions.",
    )


class SubscribeRequest(BaseSchema):
    TopicArn: Union[TopicArnSchema, str] = Field(
        min_length=1,
        max_length=256,
        alias="topic_arn",
        description="Topic ARN in which you want to subscribe",
    )
    Protocol: ProtocolEnum = Field(
        alias="protocol", description="Protocol to which you want to subscribe"
    )
    Endpoint: str = Field(alias="endpoint")
    Attributes: Optional[Union[SubscribeAttributes, Dict]] = Field(
        default=None, alias="attributes"
    )
    ReturnSubscriptionArn: Optional[bool] = Field(default=True, alias="return_subscription_arn")

    class Config:
        extra = "allow"


class SubscribeResponse(SubscriptionArnSchema):
    pass


class ConfirmSubscriptionRequest(BaseSchema):
    TopicArn: Union[TopicArnSchema, str] = Field(
        min_length=1, max_length=256, alias="topic_arn", description="Topic ARN"
    )
    Token: str = Field(
        alias="token",
        description="Short-lived token sent to an endpoint during the Subscribe action.",
    )


class Subscription(SubscriptionArnSchema):
    Owner: str = Field(description="Owner of the subscription")
    Protocol: str = Field(description="Protocol of subscription")
    Endpoint: str = Field(description="Endpoint of subscription")
    TopicArn: Union[TopicArnSchema, str] = Field(description="Topic ARN of subscription")


class ListSubscriptionsResponse(BaseModel):
    Subscriptions: List[Subscription] = Field(description="List of subscriptions")
    NextToken: Union[NextToken, str]


class ListSubscriptionTopicRequest(BaseSchema):
    TopicArn: Union[TopicArnSchema, str] = Field(
        min_length=1, max_length=256, alias="topic_arn", description="Topic ARN of subscriptions"
    )
    NextToken: Optional[str] = Field(default=None, alias="next_token", description="Next token")


class SubscribeAttributesResponse(SubscribeAttributes):
    ConfirmationWasAuthenticated: Optional[bool] = Field(
        description="Whether the subscription confirmation was authenticated."
    )
    EffectiveDeliveryPolicy: Optional[Dict] = Field(
        description="The delivery policy of the subscription."
    )
    Owner: Optional[str] = Field(description="The owner of the subscription.")
    PendingConfirmation: Optional[bool] = Field(
        description="Whether the subscription is pending confirmation (true) or not (false)."
    )
    TopicArn: Optional[Union[TopicArnSchema, str]] = Field(
        description="The topic ARN of the subscription."
    )
    SubscriptionArn: Optional[Union[SubscriptionArnSchema, str]] = Field(
        description="The subscription ARN of the subscription."
    )

    class config:
        extra = "allow"


class SetSubcribtionAttributesRequest(BaseSchema):
    SubscriptionArn: Union[SubscriptionArnSchema, str] = Field(
        min_length=1,
        max_length=256,
        alias="subscription_arn",
        description="Subscription ARN in which you want to set attributes",
    )
    AttributeName: Union[SubscribeAttributes, str] = Field(
        alias="attribute_name", description="Name of the attribute you want to set"
    )
    AttributeValue: str = Field(
        alias="attribute_value", description="Value of the attribute you want to set"
    )
