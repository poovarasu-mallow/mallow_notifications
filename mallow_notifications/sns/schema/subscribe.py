from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator

from mallow_notifications.sns.schema.base import BaseSchema, NextToken
from mallow_notifications.sns.schema.topics import TopicArnSchema


class SubscriptionArnSchema(BaseSchema):
    SubscriptionArn: str = Field(alias="subscription_arn", min_length=1, max_length=256)


class ProtocolEnum(str, Enum):
    http = "http"
    https = "https"
    email = "email"
    email_json = "email-json"
    sms = "sms"
    sqs = "sqs"
    application = "application"
    lambda_function = "lambda"
    firehose = "firehose"


class FilterPolicyScopeEnum(str, Enum):
    message_attributes = "MessageAttributes"
    message_body = "MessageBody"


class ReplayStatusEnum(str, Enum):
    COMPLETED = "Completed"
    IN_PROGRESS = "In progress"
    FAILED = "Failed"
    PENDING = "Pending"


class SubscribeAttributes(BaseModel):
    DeliveryPolicy: Optional[Dict] = Field(default=None, alias="delivery_policy")
    FilterPolicy: Optional[Dict] = Field(default=None, alias="filter_policy")
    FilterPolicyScope: Optional[Union[FilterPolicyScopeEnum, Dict]] = Field(
        default=None, alias="filter_policy_scope"
    )
    RawMessageDelivery: Optional[bool] = Field(default=None, alias="raw_message_delivery")
    RedrivePolicy: Optional[str] = Field(default=None, alias="redrive_policy")
    SubscriptionRoleArn: Optional[str] = Field(default=None, alias="subscription_role_arn")
    ReplayPolicy: Optional[str] = Field(default=None, alias="replay_policy")
    ReplayStatus: Optional[ReplayStatusEnum] = Field(default=None, alias="replay_status")


class SubscribeRequest(BaseSchema):
    TopicArn: Union[TopicArnSchema, str] = Field(min_length=1, max_length=256, alias="topic_arn")
    Protocol: ProtocolEnum = Field(alias="protocol")
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
    TopicArn: Union[TopicArnSchema, str] = Field(min_length=1, max_length=256, alias="topic_arn")
    Token: str = Field(alias="token")
    AuthenticateOnUnsubscribe: str = Field(alias="authenticate_on_unsubscribe", default=None)


class Subscription(SubscriptionArnSchema):
    Owner: str
    Protocol: str
    Endpoint: str
    TopicArn: Union[TopicArnSchema, str]


class ListSubscriptionsResponse(BaseModel):
    Subscriptions: List[Subscription]
    NextToken: Union[NextToken, str]


class ListSubscriptionTopicRequest(BaseSchema):
    TopicArn: Union[TopicArnSchema, str] = Field(min_length=1, max_length=256, alias="topic_arn")
    NextToken: Optional[str] = Field(default=None, alias="next_token")


class SubscribeAttributesResponse(SubscribeAttributes):
    ConfirmationWasAuthenticated: Optional[bool]
    EffectiveDeliveryPolicy: Optional[Dict]
    Owner: Optional[str]
    PendingConfirmation: Optional[bool]
    TopicArn: Optional[Union[TopicArnSchema, str]]
    SubscriptionArn: Optional[Union[SubscriptionArnSchema, str]]

    class config:
        extra = "allow"


class SetSubcribtionAttributesRequest(BaseSchema):
    SubscriptionArn: Union[SubscriptionArnSchema, str] = Field(
        min_length=1, max_length=256, alias="subscription_arn"
    )
    AttributeName: Union[SubscribeAttributes, str] = Field(alias="attribute_name")
    AttributeValue: str = Field(alias="attribute_value")
