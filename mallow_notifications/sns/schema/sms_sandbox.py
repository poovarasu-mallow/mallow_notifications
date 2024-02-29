from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field

from mallow_notifications.base.constants import DefaultSMSTypeEnum
from mallow_notifications.sns.schema.base import BaseSchema, NextToken


class SMSPhoneNumber(BaseSchema):
    PhoneNumber: str = Field(alias="phone_number", description="The phone number in E.164 format")


class CreateSmsSandboxPhoneNumberRequest(BaseSchema):
    PhoneNumber: Union[SMSPhoneNumber, str] = Field(
        alias="phone_number", description="The phone number in E.164 format"
    )
    LanguageCode: str = Field(
        default="en-US",
        alias="language_code",
        description="The language to use for sending the OTP",
    )


class ListSmsSandboxPhoneNumbersRequest(BaseSchema):
    NextToken: Optional[str] = Field(
        alias="next_token",
        default=None,
        desxcription="Token to specify where to start paginating. This is the NextToken from a previously truncated response.",
    )
    MaxResults: Optional[int] = Field(
        default=None, alias="max_results", description="Maximum number of phone numbers to return."
    )


class PhoneNumberStatus(BaseModel):
    PhoneNumber: Union[SMSPhoneNumber, str] = Field(description="The phone number in E.164 format")
    Status: str = Field(description="The status of the phone number")


class ListSmsSandboxPhoneNumbersResponse(BaseModel):
    PhoneNumbers: List[PhoneNumberStatus] = Field(description="List of phone numbers")
    NextToken: Optional[str] = Field(
        alias="next_token",
        default=None,
        description="Token to specify where to start paginating. This is the NextToken from a previously truncated response.",
    )


class VerifySMSSandboxPhoneNumberRequest(BaseSchema):
    PhoneNumber: Union[SMSPhoneNumber, str] = Field(
        alias="phone_number", description="The phone number in E.164 format"
    )
    OneTimePassword: str = Field(
        alias="otp", description="One-time passcode used to verify the phone number"
    )


class SMSAttributes(BaseModel):
    MonthlySpendLimit: Optional[str] = Field(
        default=None,
        alias="monthly_spend_limit",
        description="The maximum amount in USD that you are willing to spend each month to send SMS messages",
    )
    DeliveryStatusIAMRole: Optional[str] = Field(
        default=None,
        alias="delivery_status_iam_role",
        description="The IAM role that allows Amazon SNS to write logs about SMS deliveries in CloudWatch Logs.",
    )
    DeliveryStatusSuccessSamplingRate: Optional[str] = Field(
        default=None,
        alias="delivery_status_success_sampling_rate",
        description="The percentage of successful SMS deliveries for which Amazon SNS will write logs in CloudWatch Logs.",
    )
    DefaultSenderID: Optional[str] = Field(
        default=None,
        alias="default_sender_id",
        description="A string, such as your business brand, that is displayed as the sender on the receiving device",
    )
    DefaultSMSType: Optional[DefaultSMSTypeEnum] = Field(
        default=None,
        alias="default_sms_type",
        description="The type of SMS message that you want to send.",
    )
    UsageReportS3Bucket: Optional[str] = Field(
        default=None,
        alias="usage_report_s3_bucket",
        description="The name of the Amazon S3 bucket to which Amazon SNS publishes the usage report",
    )


class GetSMSAttributesRequest(BaseModel):
    attributes: List[str] = Field(alias="attributes", description="List of attributes")


class GetSMSAttributesResponse(BaseSchema):
    attributes: SMSAttributes = Field(alias="attributes", description="List of attributes")


class SetSMSAttributesRequest(BaseSchema):
    attributes: SMSAttributes = Field(alias="attributes", description="List of attributes")
