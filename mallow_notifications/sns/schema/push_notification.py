from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from mallow_notifications.base.constants import Platforms
from mallow_notifications.sns.schema.base import BaseSchema, NextToken


class PlatformApplicationArnSchema(BaseSchema):
    PlatformApplicationArn: str = Field(
        alias="platform_application_arn", min_length=1, max_length=256
    )


class PlatformApplicationAttributes(BaseSchema):
    PlatformPrincipal: Optional[str] = Field(
        alias="platform_principal",
        default=None,
        description="The principal received from the notification service",
    )
    PlatformCredential: Optional[str] = Field(
        alias="platform_credential",
        default=None,
        description="The credentials received from the notification service",
    )
    EventEndpointCreated: Optional[str] = Field(
        alias="event_endpoint_created",
        default=None,
        description="Topic ARN to which EndpointCreated event notifications are sent.",
    )
    EventEndpointDeleted: Optional[str] = Field(
        alias="event_endpoint_deleted",
        default=None,
        description="Topic ARN to which EndpointDeleted event notifications are sent.",
    )
    EventEndpointUpdated: Optional[str] = Field(
        alias="event_endpoint_updated",
        default=None,
        description="Topic ARN to which EndpointUpdated event notifications are sent.",
    )
    EventDeliveryFailure: Optional[str] = Field(
        alias="event_delivery_failure",
        default=None,
        description="Topic ARN to which DeliveryFailure event notifications are sent.",
    )
    SuccessFeedbackRoleArn: Optional[str] = Field(
        alias="success_feedback_role_arn",
        default=None,
        description="IAM role ARN used to give Amazon SNS write access to use CloudWatch Logs on your behalf.",
    )
    SuccessFeedbackSampleRate: Optional[int] = Field(
        ge=0,
        le=100,
        alias="success_feedback_sample_rate",
        default=None,
        description="Sample rate percentage (0-100) of successfully delivered messages.",
    )


class PlatformApplicationRequest(BaseSchema):
    Name: str = Field(
        min_length=1,
        max_length=256,
        alias="platform_name",
        description="Name of the platform application",
    )
    Platform: Platforms = Field(
        alias="platform_type", default=None, description="Type of platform"
    )
    Attributes: Optional[Union[PlatformApplicationAttributes, dict]] = Field(
        alias="platform_attributes",
        default=None,
        description="Additional attributes of the platform application",
    )


class PlatformApplications(BaseModel):
    PlatformApplicationArn: PlatformApplicationArnSchema = Field(
        alias="platform_application_arn",
        description="Platform application ARN",
    )
    Attributes: PlatformApplicationAttributes = Field(
        alias="platform_application_attributes",
        description="Platform application attributes",
    )


class ListPlatformApplications(BaseModel):
    PlatformApplications: List[PlatformApplications]
    NextToken: Optional[Union[NextToken, str]]


class PlatformEndpointSchema(BaseSchema):
    EndpointArn: str = Field(
        alias="endpoint_arn",
        min_length=1,
        max_length=256,
        description="Platform endpoint ARN",
    )


class PlatformEndpointAttributes(BaseModel):
    CustomUserData: str = Field(
        default=None,
        max_length=2048,
        alias="custom_user_data",
        description="Custom attributes to set when creating the endpoint",
    )
    Enabled: bool = Field(
        default=True,
        alias="enabled",
        description="Indicates whether the enabled state of the endpoint.",
    )
    Token: str = Field(
        max_length=2048,
        alias="token",
        description="Device token, also referred to as a registration id, for an app and mobile device.",
    )


class PlatformEndpointRequest(BaseSchema):
    PlatformApplicationArn: Union[PlatformApplicationArnSchema, str] = Field(
        min_length=1,
        max_length=256,
        alias="platform_application_arn",
        description="Platform application ARN",
    )
    Token: str = Field(
        alias="device_token",
        description="Device token, also referred to as a registration id, for an app and mobile device.",
    )
    CustomUserData: str = Field(
        default=None,
        alias="custom_user_data",
        max_length=2000,
        description="Custom attributes to set when creating the endpoint",
    )
    Attributes: Optional[Union[PlatformEndpointAttributes, dict]] = Field(
        alias="platform_endpoint_attributes",
        default=None,
        description="Additional attributes of the platform endpoint",
    )


class GetEndpointAttributesResponse(BaseModel):
    Attributes: Dict[str, str] = Field(
        alias="attributes", description="Custom attributes for the endpoint"
    )
