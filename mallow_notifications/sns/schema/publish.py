from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from mallow_notifications.sns.endpoints.topics import TopicArnSchema
from mallow_notifications.sns.schema.base import BaseSchema
from mallow_notifications.base.constants import MessageAttributeDataTypes





class MessageAttribute(BaseModel):
    DataType: MessageAttributeDataTypes = Field(alias="data_type", default=None)
    StringValue: Optional[str] = Field(default=None, alias="string_value")
    BinaryValue: Optional[bytes] = Field(default=None, alias="binary_value")


class PublishRequest(BaseSchema):
    TopicArn: Optional[Union[TopicArnSchema, str]] = Field(
        default=None, min_length=1, max_length=256, alias="topic_arn"
    )
    TargetArn: Optional[str] = Field(default=None, alias="target_arn")
    PhoneNumber: Optional[str] = Field(default=None, alias="phone_number")
    Message: Union[str, dict] = Field(alias="message")
    Subject: Optional[str] = Field(alias="subject", default=None)
    MessageStructure: Optional[str] = Field(default="json", alias="message_structure")
    MessageAttributes: Optional[Dict[str, MessageAttribute]] = Field(
        default=None, alias="message_attributes"
    )
    MessageDeduplicationId: Optional[str] = Field(
        default=None, alias="message_deduplication_id", max_length=128
    )
    MessageGroupId: Optional[str] = Field(default=None, alias="message_group_id", max_length=128)


class PublishResponse(BaseModel):
    MessageId: str = Field(max_length=128)
    SequenceNumber: str


class PublishBatchRequestEntry(BaseModel):
    Id: str = Field(alias="id")
    Message: str = Field(alias="message")
    Subject: Optional[str] = Field(alias="subject")
    MessageStructure: Optional[str] = Field(alias="message_structure")
    MessageAttributes: Optional[Dict[MessageAttribute, str]] = Field(alias="message_attributes")
    MessageDeduplicationId: Optional[str] = Field(alias="message_deduplication_id", max_length=128)
    MessageGroupId: Optional[str] = Field(alias="message_group_id", max_length=128)


class PublishBatchRequest(BaseSchema):
    TopicArn: str = Field(min_length=1, max_length=256, alias="topic_arn")
    PublishBatchRequestEntries: List[Union[PublishBatchRequestEntry, dict]] = Field(
        alias="publish_batch_request_entries"
    )


class PublishBatchResponseSuccessEntry(BaseModel):
    Id: str
    MessageId: str
    SequenceNumber: str


class PublishBatchResponseErrorEntry(BaseModel):
    Id: str
    Code: str
    Message: str
    SenderFault: bool


class PublishBatchResponse(BaseModel):
    Successful: List[PublishBatchResponseSuccessEntry]
    Failed: List[PublishBatchResponseErrorEntry]
