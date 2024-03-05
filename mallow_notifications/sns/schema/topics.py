from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from mallow_notifications.sns.schema.base import BaseSchema, NextToken


class TopicArnSchema(BaseSchema):
    TopicArn: str = Field(min_length=1, max_length=256, alias="topic_arn", description="Topic ARN")


class TopicAttributes(BaseModel):
    DeliveryPolicy: Optional[Dict] = Field(
        default=None,
        alias="delivery_policy",
        description="Policy that defines how Amazon SNS retries failed deliveries to HTTP/S endpoints",
    )
    DisplayName: Optional[str] = Field(
        default=None,
        alias="display_name",
        description="Display name to use for a topic with SMS subscriptions",
    )
    FifoTopic: Optional[bool] = Field(
        default=None, alias="fifo_topic", description="Set to true to create a FIFO topic"
    )
    Policy: Optional[Dict] = Field(
        default=None,
        alias="policy",
        description="The policy that defines who can access your topic",
    )
    SignatureVersion: Optional[str] = Field(
        default=None, alias="signature_version", description="The signature version of your topic"
    )
    TracingConfig: Optional[Dict[str, bool]] = Field(
        default=None, alias="tracing_config", description="Tracing mode of an Amazon SNS topic"
    )
    KmsMasterKeyId: Optional[str] = Field(
        default=None, alias="kms_master_key_id", description="KMS master key ID used for the topic"
    )


class Tag(BaseModel):
    Key: str = Field(min_length=1, max_length=128, alias="key", description="Tag key")
    Value: str = Field(min_length=0, max_length=256, alias="value", description="Tag value")


class CreateTopicRequest(BaseSchema):
    Name: str = Field(
        min_length=1,
        max_length=256,
        alias="topic_name",
        description="Name of the topic you want to create",
    )
    Attributes: Optional[Union[TopicAttributes, Dict[str, str]]] = Field(
        default=None,
        alias="topic_attributes",
        description="Attributes of the topic you want to create",
    )
    Tags: Optional[List[Union[Tag, Dict[str, str]]]] = Field(
        default=None,
        alias="topic_tags",
        description="Tags to apply to the topic you want to create",
    )
    DataProtectionPolicy: Optional[str] = Field(
        max_length=30720,
        default=None,
        alias="topic_data_protection_policy",
        description="Data protection policy of the topic you want to create",
    )


class TopicArnResoponse(BaseModel):
    TopicArn: TopicArnSchema = Field(alias="topic_arn", description="Topic ARN")


class ListTopicsResponse(BaseModel):
    Topics: List[TopicArnResoponse] = Field(alias="topics", description="List of topic ARNs")
    NextToken: Union[NextToken, str]


class AttributesNames(BaseModel):
    DeliveryPolicy: Optional[Dict] = Field(
        default=None,
        alias="delivery_policy",
        description="Policy that defines how Amazon SNS retries failed deliveries to HTTP/S endpoints",
    )
    DisplayName: Optional[str] = Field(
        default=None,
        alias="display_name",
        description="Display name to use for a topic with SMS subscriptions",
    )
    Policy: Optional[Dict] = Field(
        default=None,
        alias="policy",
        description="The policy that defines who can access your topic",
    )
    TracingConfig: Optional[Union[dict, str]] = Field(
        default=None, alias="tracing_config", description="Tracing mode of an Amazon SNS topic"
    )
    HTTPSuccessFeedbackRoleArn: Optional[str] = Field(
        default=None,
        alias="http_success_feedback_role_arn",
        description="Successful message delivery status for an Amazon SNS topic that is subscribed to an HTTP endpoint",
    )
    HTTPFailureFeedbackRoleArn: Optional[str] = Field(
        default=None,
        alias="http_failure_feedback_role_arn",
        description="Failed message delivery status for an Amazon SNS topic that is subscribed to an HTTP endpoint",
    )
    HTTPSuccessFeedbackSampleRate: Optional[float] = Field(
        default=None,
        alias="http_success_feedback_sample_rate",
        description="Indicates percentage of successful messages to sample for an Amazon SNS topic that is subscribed to an HTTP endpoint.",
    )
    FirehoseSuccessFeedbackRoleArn: Optional[str] = Field(
        default=None,
        alias="firehose_success_feedback_role_arn",
        description="Successful message delivery status for an Amazon SNS topic that is subscribed to an Firehose endpoint",
    )
    FirehoseFailureFeedbackRoleArn: Optional[str] = Field(
        default=None,
        alias="firehose_failure_feedback_role_arn",
        description="Failed message delivery status for an Amazon SNS topic that is subscribed to an Firehose endpoint",
    )
    FirehoseSuccessFeedbackSampleRate: Optional[float] = Field(
        default=None,
        alias="firehose_success_feedback_sample_rate",
        description="Indicates percentage of successful messages to sample for an Amazon SNS topic that is subscribed to an Amazon Kinesis Data Firehose endpoint.",
    )
    LambdaSuccessFeedbackRoleArn: Optional[str] = Field(
        default=None,
        alias="lambda_success_feedback_role_arn",
        description="Successful message delivery status for an Amazon SNS topic that is subscribed to an Lambda endpoint",
    )
    LambdaFailureFeedbackRoleArn: Optional[str] = Field(
        default=None,
        alias="lambda_failure_feedback_role_arn",
        description="Failed message delivery status for an Amazon SNS topic that is subscribed to an Lambda endpoint",
    )
    LambdaSuccessFeedbackSampleRate: Optional[float] = Field(
        default=None,
        alias="lambda_success_feedback_sample_rate",
        description="Indicates percentage of successful messages to sample for an Amazon SNS topic that is subscribed to an Lambda endpoint.",
    )
    ApplicationSuccessFeedbackRoleArn: Optional[str] = Field(
        default=None,
        alias="application_success_feedback_role_arn",
        description="Successful message delivery status for an Amazon SNS topic that is subscribed to an Amazon Kinesis Data Firehose endpoint",
    )
    ApplicationFailureFeedbackRoleArn: Optional[str] = Field(
        default=None,
        alias="application_failure_feedback_role_arn",
        description="Failed message delivery status for an Amazon SNS topic that is subscribed to an Amazon Kinesis Data Firehose endpoint",
    )
    ApplicationSuccessFeedbackSampleRate: Optional[float] = Field(
        default=None,
        alias="application_success_feedback_sample_rate",
        description="Indicates percentage of successful messages to sample for an Amazon SNS topic that is subscribed to an Amazon Kinesis Data Firehose endpoint.",
    )
    SQSSuccessFeedbackRoleArn: Optional[str] = Field(
        default=None,
        alias="sqs_success_feedback_role_arn",
        description="Successful message delivery status for an Amazon SNS topic that is subscribed to an Amazon SQS endpoint",
    )
    SQSFailureFeedbackRoleArn: Optional[str] = Field(
        default=None,
        alias="sqs_failure_feedback_role_arn",
        description="Failed message delivery status for an Amazon SNS topic that is subscribed to an Amazon SQS endpoint",
    )
    SQSSuccessFeedbackSampleRate: Optional[float] = Field(
        default=None,
        alias="sqs_success_feedback_sample_rate",
        description="Indicates percentage of successful messages to sample for an Amazon SNS topic that is subscribed to an Amazon SQS endpoint.",
    )
    KmsMasterKeyId: Optional[str] = Field(
        default=None,
        alias="kms_master_key_id",
        description="The ID of an AWS-managed customer master key (CMK) for Amazon SNS or a custom CMK.",
    )
    SignatureVersion: Optional[int] = Field(
        default=None,
        alias="signature_version",
        description="Signature version of an Amazon SNS topic",
    )
    ContentBasedDeduplication: Optional[bool] = Field(
        default=None,
        alias="content_based_deduplication",
        description="Indicates whether content-based deduplication is enabled for an Amazon SNS topic",
    )


class SetTopicAttributesRequest(BaseSchema):
    TopicArn: Union[TopicArnSchema, str] = Field(
        min_length=1,
        max_length=256,
        alias="topic_arn",
        description="Topic ARN to modify attributes for",
    )
    AttributeName: Union[AttributesNames, str] = Field(
        alias="attribute_name", description="The name of the attribute you want to modify"
    )
    AttributeValue: str = Field(
        alias="attribute_value", description="The new value for the attribute"
    )


class GetTopicAttributes(TopicAttributes):
    EffectiveDeliveryPolicy: Optional[Dict] = Field(
        description="The delivery policy of the topic."
    )
    Owner: Optional[str] = Field(description="The owner of the topic.")
    SubscriptionsConfirmed: Optional[int] = Field(
        description="The number of confirmed subscriptions for the topic."
    )
    SubscriptionsDeleted: Optional[int] = Field(
        description="The number of deleted subscriptions for the topic."
    )
    SubscriptionsPending: Optional[int] = Field(
        description="The number of pending subscriptions for the topic."
    )
    TopicArn: Optional[TopicArnSchema] = Field(description="The topic ARN.")
    ContentBasedDeduplication: Optional[bool] = Field(
        description="Indicates whether content-based deduplication is enabled for the topic."
    )


class GetTopicAttributesResponse(BaseModel):
    Attributes: Optional[Dict[str, GetTopicAttributes]] = Field(
        description="The attributes of the topic."
    )
