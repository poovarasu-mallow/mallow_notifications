from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field

from mallow_notifications.sns.schema.base import BaseSchema, NextToken


class SMSPhoneNumber(BaseSchema):
    PhoneNumber: str = Field(alias="phone_number")


class CreateSmsSandboxPhoneNumberRequest(BaseSchema):
    PhoneNumber: Union[SMSPhoneNumber, str] = Field(alias="phone_number")
    LanguageCode: str = Field(default="en-US", alias="language_code")


class ListSmsSandboxPhoneNumbersRequest(BaseSchema):
    NextToken: Optional[str] = Field(alias="next_token", default=None)
    MaxResults: Optional[int] = Field(default=None, alias="max_results")


class PhoneNumberStatus(BaseModel):
    PhoneNumber: Union[SMSPhoneNumber, str]
    Status: str


class ListSmsSandboxPhoneNumbersResponse(BaseModel):
    PhoneNumbers: List[PhoneNumberStatus]
    NextToken: Optional[Union[NextToken, str]]


class VerifySMSSandboxPhoneNumberRequest(BaseSchema):
    PhoneNumber: Union[SMSPhoneNumber, str] = Field(alias="phone_number")
    OneTimePassword: str = Field(alias="otp")


class DefaultSMSTypeEnum(str, Enum):
    Promotional = "Promotional"
    Transactional = "Transactional"


class SMSAttributes(BaseModel):
    MonthlySpendLimit: Optional[str] = Field(default=None, alias="monthly_spend_limit")
    DeliveryStatusIAMRole: Optional[str] = Field(default=None, alias="delivery_status_iam_role")
    DeliveryStatusSuccessSamplingRate: Optional[str] = Field(
        default=None, alias="delivery_status_success_sampling_rate"
    )
    DefaultSenderID: Optional[str] = Field(default=None, alias="default_sender_id")
    DefaultSMSType: Optional[DefaultSMSTypeEnum] = Field(default=None, alias="default_sms_type")
    UsageReportS3Bucket: Optional[str] = Field(default=None, alias="usage_report_s3_bucket")


class GetSMSAttributesRequest(BaseModel):
    attributes: List[str]


class GetSMSAttributesResponse(BaseSchema):
    attributes: SMSAttributes


class SetSMSAttributesRequest(BaseSchema):
    attributes: SMSAttributes
