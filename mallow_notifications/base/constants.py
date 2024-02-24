"""Modules contains the list of constants used in the library."""


# List of accepted protocols while sending the notification through Amazon SNS
PUBLISH_MESSAGE_PROTOCOLS = {
    "EMAIL": "email",
    "SQS": "sqs",
    "LAMBDA": "lambda",
    "HTTP": "http",
    "HTTPS": "https",
    "SMS": "sms",
    "FIREHOSE": "firehose",
    "APNS": "APNS",
    "APNS_SANDBOX": "APNS_SANDBOX",
    "APNS_VOIP": "APNS_VOIP",
    "APNS_VOIP_SANDBOX": "APNS_VOIP_SANDBOX",
    "MACOS": "MACOS",
    "MACOS_SANDBOX": "MACOS_SANDBOX",
    "GCM": "GCM",
    "ADM": "ADM",
    "BAIDU": "BAIDU",
    "MPNS": "MPNS",
    "WNS": "WNS",
}


SMS_SANDBOX_PHONE_NUMBER_STATUS_VERIFIED = "Verified"
SMS_SANDBOX_PHONE_NUMBER_STATUS_PENDING = "Pending"

# SNS sms types
SMS_TYPE_PROMOTIONAL = "Promotional"
SMS_TYPE_TRANSACTIONAL = "Transactional"
