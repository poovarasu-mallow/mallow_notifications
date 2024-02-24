from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator

from mallow_notifications.sns.schema.base import BaseSchema, NextToken


class TopicArnSchema(BaseSchema):
    TopicArn: str = Field(min_length=1, max_length=256, alias="topic_arn")


class TopicAttributes(BaseModel):
    DeliveryPolicy: Optional[Dict] = Field(default=None, alias="delivery_policy")
    DisplayName: Optional[str] = Field(default=None, alias="display_name")
    FifoTopic: Optional[bool] = Field(default=None, alias="fifo_topic")
    Policy: Optional[Dict] = Field(default=None, alias="policy")
    SignatureVersion: Optional[str] = Field(default=None, alias="signature_version")
    TracingConfig: Optional[Dict[str, bool]] = Field(default=None, alias="tracing_config")
    KmsMasterKeyId: Optional[str] = Field(default=None, alias="kms_master_key_id")


class Tag(BaseModel):
    Key: str = Field(min_length=1, max_length=128, alias="key")
    Value: str = Field(min_length=0, max_length=256, alias="value")


class CreateTopicRequest(BaseSchema):
    Name: str = Field(min_length=1, max_length=256, alias="topic_name")
    Attributes: Optional[Union[TopicAttributes, Dict[str, str]]] = Field(
        default=None, alias="topic_attributes"
    )
    Tags: Optional[List[Union[Tag, Dict[str, str]]]] = Field(default=None, alias="topic_tags")
    DataProtectionPolicy: Optional[str] = Field(
        max_length=30720, default=None, alias="topic_data_protection_policy"
    )


class TopicArnResoponse(BaseModel):
    TopicArn: TopicArnSchema


class ListTopicsResponse(BaseModel):
    Topics: List[TopicArnResoponse]
    NextToken: Union[NextToken, str]


class TracingConfigSchema(BaseModel):
    Enabled: Optional[bool]
    IncludeFirehose: Optional[bool]
    IncludeExternalId: Optional[bool]
    IncludeLogRoot: Optional[bool]
    IncludeOrganization: Optional[bool]
    UseExistingActiveTraceHeader: Optional[bool]
    Sampled: Optional[bool]


class AttributesNames(BaseModel):
    DeliveryPolicy: Optional[Dict] = Field(default=None, alias="delivery_policy")
    DisplayName: Optional[str] = Field(default=None, alias="display_name")
    Policy: Optional[Dict] = Field(default=None, alias="policy")
    TracingConfig: Optional[TracingConfigSchema] = Field(default=None, alias="tracing_config")
    HTTPSuccessFeedbackRoleArn: Optional[str] = Field(
        default=None, alias="http_success_feedback_role_arn"
    )
    HTTPFailureFeedbackRoleArn: Optional[str] = Field(
        default=None, alias="http_failure_feedback_role_arn"
    )
    HTTPSuccessFeedbackSampleRate: Optional[float] = Field(
        default=None, alias="http_success_feedback_sample_rate"
    )
    FirehoseSuccessFeedbackRoleArn: Optional[str] = Field(
        default=None, alias="firehose_success_feedback_role_arn"
    )
    FirehoseFailureFeedbackRoleArn: Optional[str] = Field(
        default=None, alias="firehose_failure_feedback_role_arn"
    )
    FirehoseSuccessFeedbackSampleRate: Optional[float] = Field(
        default=None, alias="firehose_success_feedback_sample_rate"
    )
    LambdaSuccessFeedbackRoleArn: Optional[str] = Field(
        default=None, alias="lambda_success_feedback_role_arn"
    )
    LambdaFailureFeedbackRoleArn: Optional[str] = Field(
        default=None, alias="lambda_failure_feedback_role_arn"
    )
    LambdaSuccessFeedbackSampleRate: Optional[float] = Field(
        default=None, alias="lambda_success_feedback_sample_rate"
    )
    ApplicationSuccessFeedbackRoleArn: Optional[str] = Field(
        default=None, alias="application_success_feedback_role_arn"
    )
    ApplicationFailureFeedbackRoleArn: Optional[str] = Field(
        default=None, alias="application_failure_feedback_role_arn"
    )
    ApplicationSuccessFeedbackSampleRate: Optional[float] = Field(
        default=None, alias="application_success_feedback_sample_rate"
    )
    SQSSuccessFeedbackRoleArn: Optional[str] = Field(
        default=None, alias="sqs_success_feedback_role_arn"
    )
    SQSFailureFeedbackRoleArn: Optional[str] = Field(
        default=None, alias="sqs_failure_feedback_role_arn"
    )
    SQSSuccessFeedbackSampleRate: Optional[float] = Field(
        default=None, alias="sqs_success_feedback_sample_rate"
    )
    KmsMasterKeyId: Optional[str] = Field(default=None, alias="kms_master_key_id")
    SignatureVersion: Optional[int] = Field(default=None, alias="signature_version")
    ContentBasedDeduplication: Optional[bool] = Field(
        default=None, alias="content_based_deduplication"
    )


class SetTopicAttributesRequest(BaseSchema):
    TopicArn: Union[TopicArnSchema, str] = Field(min_length=1, max_length=256, alias="topic_arn")
    AttributeName: Union[AttributesNames, str] = Field(alias="attribute_name")
    AttributeValue: str = Field(alias="attribute_value")


class GetTopicAttributes(TopicAttributes):
    EffectiveDeliveryPolicy: Optional[Dict]
    Owner: Optional[str]
    SubscriptionsConfirmed: Optional[int]
    SubscriptionsDeleted: Optional[int]
    SubscriptionsPending: Optional[int]
    TopicArn: Optional[TopicArnSchema]
    ContentBasedDeduplication: Optional[bool]


class GetTopicAttributesResponse(BaseModel):
    Attributes: Optional[Dict[str, GetTopicAttributes]]
