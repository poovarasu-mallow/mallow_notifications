from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from mallow_notifications.base.constants import MessageAttributeDataTypes
from mallow_notifications.sns.endpoints.topics import TopicArnSchema
from mallow_notifications.sns.schema.base import BaseSchema


class MessageAttribute(BaseModel):
    DataType: MessageAttributeDataTypes = Field(
        alias="data_type", default=None, description="Stores a message attribute data type."
    )
    StringValue: Optional[str] = Field(
        default=None, alias="string_value", description="Stores a string value."
    )
    BinaryValue: Optional[bytes] = Field(
        default=None,
        alias="binary_value",
        description="Stores binary data, such as compressed, encrypted, or images.",
    )


class PublishRequest(BaseSchema):
    TopicArn: Optional[Union[TopicArnSchema, str]] = Field(
        default=None,
        min_length=1,
        max_length=256,
        alias="topic_arn",
        description="Topic ARN in which you want to publish",
    )
    TargetArn: Optional[str] = Field(
        default=None, alias="target_arn", description="Target ARN in which you want to publish"
    )
    PhoneNumber: Optional[str] = Field(
        default=None,
        alias="phone_number",
        description="Phone number to which you want to deliver an SMS message. Use E.164 format",
    )
    Message: Union[str, dict] = Field(alias="message", description="Message to be sent")
    Subject: Optional[str] = Field(
        alias="subject", default=None, description="Subject of the message"
    )
    MessageStructure: Optional[str] = Field(
        default="json",
        alias="message_structure",
        description="Structure of the message, such as html, plaint, etc",
    )
    MessageAttributes: Optional[Dict[str, MessageAttribute]] = Field(
        default=None,
        alias="message_attributes",
        description="Additional attributes of the message",
    )
    MessageDeduplicationId: Optional[str] = Field(
        default=None,
        alias="message_deduplication_id",
        max_length=128,
        description="Token for deduplicating messages in FIFO topics and it must be unique and overrides system-generated ID if provided.",
    )
    MessageGroupId: Optional[str] = Field(
        default=None,
        alias="message_group_id",
        max_length=128,
        description="Tag for FIFO (first-in-first-out) topics Identifies messages belonging to the same groupand must be unique for each message.",
    )


class PublishResponse(BaseModel):
    MessageId: str = Field(max_length=128, description="Message ID of the published message")
    SequenceNumber: str = Field(
        max_length=128, description="Sequence number of the published message"
    )


class PublishBatchRequestEntry(BaseModel):
    Id: str = Field(alias="id", description="Id of the published message")
    Message: str = Field(alias="message", description="Message to be sent")
    Subject: Optional[str] = Field(
        alias="subject", default=None, description="Subject of the message"
    )
    MessageStructure: Optional[str] = Field(
        alias="message_structure",
        description="Structure of the message, such as html, plaint, etc",
    )
    MessageAttributes: Optional[Dict[str, MessageAttribute]] = Field(
        default=None,
        alias="message_attributes",
        description="Additional attributes of the message",
    )
    MessageDeduplicationId: Optional[str] = Field(
        default=None,
        alias="message_deduplication_id",
        max_length=128,
        description="Token for deduplicating messages in FIFO topics and it must be unique and overrides system-generated ID if provided.",
    )
    MessageGroupId: Optional[str] = Field(
        default=None,
        alias="message_group_id",
        max_length=128,
        description="Tag for FIFO (first-in-first-out) topics Identifies messages belonging to the same groupand must be unique for each message.",
    )


class PublishBatchRequest(BaseSchema):
    TopicArn: str = Field(
        min_length=1,
        max_length=256,
        alias="topic_arn",
        description="The Amazon resource name (ARN) of the topic you want to batch publish.",
    )
    PublishBatchRequestEntries: List[Union[PublishBatchRequestEntry, dict]] = Field(
        alias="publish_batch_request_entries",
        description="A list of PublishBatch request entries to be sent to the SNS topic",
    )


class PublishBatchResponseSuccessEntry(BaseModel):
    Id: str = Field(alias="id", description="Id of the published message")
    MessageId: str = Field(alias="message_id", description="Message ID of the published message")
    SequenceNumber: str = Field(
        alias="sequence_number", description="Sequence number of the published message"
    )


class PublishBatchResponseErrorEntry(BaseModel):
    Id: str = Field(alias="id", description="Id of the published message")
    Code: str = Field(
        description="An error code representing why the action failed on this entry."
    )
    Message: str = Field(
        description="An error message explaining why the action failed on this entry."
    )
    SenderFault: bool = Field(
        description="Specifies whether the error happened due to the caller of the batch API action."
    )


class PublishBatchResponse(BaseModel):
    Successful: List[PublishBatchResponseSuccessEntry] = Field(
        description="List of successfully published messages"
    )
    Failed: List[PublishBatchResponseErrorEntry] = Field(description="List of failed messages")
