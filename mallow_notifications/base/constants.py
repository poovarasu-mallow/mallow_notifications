"""Modules contains the list of constants used in the library."""

from enum import Enum


# pylint: disable=invalid-name
class PublishMessageProtocol(str, Enum):
    """Enum class for PublishMessageProtocol."""

    EMAIL = "email"
    TOPIC = "topic"
    PUSH = "push"
    PUSH_NOTIFICATION = "push_notification"
    SMS = "sms"
    SMS_SANDBOX = "sms_sandbox"


SMS_SANDBOX_PHONE_NUMBER_STATUS_VERIFIED = "Verified"
SMS_SANDBOX_PHONE_NUMBER_STATUS_PENDING = "Pending"

# SNS sms types
SMS_TYPE_PROMOTIONAL = "Promotional"
SMS_TYPE_TRANSACTIONAL = "Transactional"


# pylint: disable=invalid-name
class MessageAttributeDataTypes(str, Enum):
    """Enum class for MessageAttributeDataTypes."""

    String = "String"
    StringArray = "String.Array"
    Number = "Number"
    Binary = "Binary"


# pylint: disable=invalid-name
class Platforms(str, Enum):
    """Enum class for Platforms."""

    ADM = "ADM"
    Baidu = "Baidu"
    APNS = "APNS"
    APNS_SANDBOX = "APNS_SANDBOX"
    GCM = "GCM"
    MPNS = "MPNS"
    WNS = "WNS"


# pylint: disable=invalid-name
class DefaultSMSTypeEnum(str, Enum):
    """Enum class for DefaultSMSTypeEnum."""

    Promotional = "Promotional"
    Transactional = "Transactional"


# pylint: disable=invalid-name
class ProtocolEnum(str, Enum):
    """Enum class for ProtocolEnum."""

    http = "http"
    https = "https"
    email = "email"
    email_json = "email-json"
    sms = "sms"
    sqs = "sqs"
    application = "application"
    lambda_function = "lambda"
    firehose = "firehose"


# pylint: disable=invalid-name
class FilterPolicyScopeEnum(str, Enum):
    """Enum class for FilterPolicyScopeEnum."""

    message_attributes = "MessageAttributes"
    message_body = "MessageBody"


# pylint: disable=invalid-name
class ReplayStatusEnum(str, Enum):
    """Enum class for ReplayStatusEnum."""

    COMPLETED = "Completed"
    IN_PROGRESS = "In progress"
    FAILED = "Failed"
    PENDING = "Pending"
