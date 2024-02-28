from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from mallow_notifications.sns.schema.base import BaseSchema, NextToken
from mallow_notifications.base.constants import Platforms


class PlatformApplicationArnSchema(BaseSchema):
    PlatformApplicationArn: str = Field(
        alias="platform_application_arn", min_length=1, max_length=256
    )


class PlatformApplicationAttributes(BaseSchema):
    PlatformPrincipal: Optional[str] = Field(alias="platform_principal", default=None)
    PlatformCredential: Optional[str] = Field(alias="platform_credential", default=None)
    EventEndpointCreated: Optional[str] = Field(alias="event_endpoint_created", default=None)
    EventEndpointDeleted: Optional[str] = Field(alias="event_endpoint_deleted", default=None)
    EventEndpointUpdated: Optional[str] = Field(alias="event_endpoint_updated", default=None)
    EventDeliveryFailure: Optional[str] = Field(alias="event_delivery_failure", default=None)
    SuccessFeedbackRoleArn: Optional[str] = Field(alias="success_feedback_role_arn", default=None)
    FailureFeedbackRoleArn: Optional[str] = Field(alias="failure_feedback_role_arn", default=None)
    SuccessFeedbackSampleRate: Optional[int] = Field(
        ge=0, le=100, alias="success_feedback_sample_rate", default=None
    )


class PlatformApplicationRequest(BaseSchema):
    Name: str = Field(min_length=1, max_length=256, alias="platform_name")
    Platform: Platforms = Field(alias="platform_type", default=None)
    Attributes: Optional[Union[PlatformApplicationAttributes, dict]] = Field(
        alias="platform_attributes", default=None
    )


class PlatformApplications(BaseModel):
    PlatformApplicationArn: PlatformApplicationArnSchema
    Attributes: PlatformApplicationAttributes


class ListPlatformApplications(BaseModel):
    PlatformApplications: List[PlatformApplications]
    NextToken: Optional[Union[NextToken, str]]


class PlatformEndpointSchema(BaseSchema):
    EndpointArn: str = Field(alias="endpoint_arn", min_length=1, max_length=256)


class PlatformEndpointAttributes(BaseModel):
    CustomUserData: str = Field(default=None, max_length=2048, alias="custom_user_data")
    Enabled: bool = Field(default=True, alias="enabled")
    Token: str = Field(max_length=2048, alias="token")


class PlatformEndpointRequest(BaseSchema):
    PlatformApplicationArn: Union[PlatformApplicationArnSchema, str] = Field(
        min_length=1, max_length=256, alias="platform_application_arn"
    )
    Token: str = Field(alias="device_token")
    CustomUserData: str = Field(default=None, alias="custom_user_data", max_length=2000)
    Attributes: Optional[Union[PlatformEndpointAttributes, dict]] = Field(
        alias="platform_endpoint_attributes", default=None
    )


class GetEndpointAttributesResponse(BaseModel):
    Attributes: Dict[str, str] = Field(alias="attributes")
