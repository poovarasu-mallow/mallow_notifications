"""This module provides the `Notification` class, which is used to send
notifications using the Amazon SNS service."""
import json
from typing import Optional

from mallow_notifications.base.celery import celery
from mallow_notifications.base.exceptions import NotificationError
from mallow_notifications.base.utils import check_required_attributes
from mallow_notifications.sns import (
    SNSPublishMessage,
    SNSPushNotification,
    SNSSandboxSMS,
    SNSTopics,
    SNSTopicSubscribe,
)
from mallow_notifications.sns.notification import (
    SendPushNotification,
    SendSMS,
    SendTopicMessage,
)


def get_driver(service: str):
    """Returns the driver class for the specified service.

    :params service (str): The type of service to use, such as "topic",
        "subscribe", "email", "push", or "sms".
    :raises NotificationError: If the specified service is not a valid
        service.
    :returns: The driver class for the specified service.
    """
    if service in ("topic", "subscribe", "email"):
        base = SendTopicMessage
    elif service in ("push", "push_notification"):
        base = SendPushNotification
    elif service in ("sms", "sms_sandbox"):
        base = SendSMS
    else:
        raise NotificationError("Invalid service.")
    return base()


class Notification:
    """Class for sending notifications using the Amazon SNS service."""

    # pylint: disable=too-many-instance-attributes, too-many-arguments, too-many-locals
    def __init__(
        self,
        run_asynk_task=False,
        topic_arn: Optional[str] = None,
        target_arn: Optional[str] = None,
        phone_number: Optional[str] = None,
        subject: Optional[str] = None,
        title: Optional[str] = None,
        message: Optional[str] = None,
        service: Optional[str] = None,
        protocol: Optional[str] = None,
        message_structure: Optional[str] = "json",
        message_deduplication_id: Optional[str] = None,
        message_group_id: Optional[str] = None,
        badge: Optional[int] = None,
        device_token: Optional[str] = None,
        device_type: Optional[str] = None,
        **kwargs,
    ):
        self.run_asynk_task = run_asynk_task
        self.push_notification = SNSPushNotification()
        self.publish = SNSPublishMessage()
        self.sms = SNSSandboxSMS()
        self.topic = SNSTopics()
        self.subscribe = SNSTopicSubscribe()
        self.topic_arn = topic_arn
        self.target_arn = target_arn
        self.phone_number = phone_number
        self.subject = subject
        self.title = title
        self.message = message
        self.service = service
        self.protocol = protocol
        self.message_structure = message_structure
        self.message_deduplication_id = message_deduplication_id
        self.message_group_id = message_group_id
        self.badge = badge
        self.device_token = device_token
        self.device_type = device_type
        self.content = {}
        self.attributes = {}
        self.data = {}
        self.sound = kwargs.get("sound", None)
        self.email_message = kwargs.get("email_message", None)
        self.sqs_message = kwargs.get("sqs_message", None)
        self.lambda_message = kwargs.get("lambda_message", None)
        self.http_message = kwargs.get("http_message", None)
        self.https_message = kwargs.get("https_message", None)
        self.sms_message = kwargs.get("sms_message", None)
        self.firehose_message = kwargs.get("firehose_message", None)
        self.apns_message = kwargs.get("apns_message", None)
        self.apns_voip_message = kwargs.get("apns_sandbox_message", None)
        self.macos_message = kwargs.get("apns_sandbox_message", None)
        self.gcm_message = kwargs.get("gcm_message", None)
        self.adm_message = kwargs.get("adm_message", None)
        self.baidu_message = kwargs.get("baidu_message", None)
        self.mpns_message = kwargs.get("mpns_message", None)
        self.wns_message = kwargs.get("wns_message", None)

    # pylint: disable=line-too-long, consider-using-f-string
    def _get_gcm_message(self, message):
        """Returns a GCM message with the specified title, text, body, sound,
        and data.

        :param message: A dictionary containing the GCM message details.
        :type message: dict
        :return: A string representing the GCM message.
        :rtype: str
        """
        message = "{{ notification: {{ title: {title}, text: {text}, body: {body}, sound: {sound} }}, data: {data} }}".format(
            title=self.title,
            text=self.message if self.gcm_message is None else self.gcm_message,
            body=self.message if self.gcm_message is None else self.gcm_message,
            sound="default" if self.sound is None else self.sound,
            data=self.data,
        )
        return message

    # pylint: disable=line-too-long, consider-using-f-string
    def _apns_message(self, message):
        """Returns an APNS message with the specified title, sound, and data.

        :param message: A dictionary containing the APNS message
            details.
        :type message: dict
        :return: A string representing the APNS message.
        :rtype: str
        """
        if self.badge is None:
            message = (
                '"{{ "aps": {{ "alert": {title},"sound": {sound} }}, "acme2": {data}}}"'.format(
                    title=self.title,
                    sound="default" if self.sound is None else self.sound,
                    data=self.data,
                )
            )
        else:
            message = '{{ "aps": {{ "alert": {title},"sound": {sound}, "badge": {badge}}}, "acme2": {data}}}'.format(
                title=self.title,
                sound="default" if self.sound is None else self.sound,
                badge=self.badge,
                data=self.data,
            )
        return message

    def message_payloads(self, message: str):
        """Returns a dictionary of message payloads with the specified message.

        :param message: A string representing the message.
        :type message: str
        :return: A dictionary of message payloads.
        :rtype: dict
        """
        message = {
            "default": message,
            "email": message if self.email_message is None else self.email_message,
            "sqs": message if self.sqs_message is None else self.sqs_message,
            "lambda": message if self.lambda_message is None else self.lambda_message,
            "http": message if self.http_message is None else self.http_message,
            "https": message if self.https_message is None else self.https_message,
            "sms": message if self.sms_message is None else self.sms_message,
            "GCM": self._get_gcm_message(message),
            "APNS": self._apns_message(message),
            "APNS_SANDBOX": self._apns_message(message),
            "APNS_VOIP": self._apns_message(message),
            "APNS_VOIP_SANDBOX": self._apns_message(message),
            "MACOS": self._apns_message(message),
            "MACOS_SANDBOX": self._apns_message(message),
        }
        return message

    def set_content(self, message_structure, message):
        """Sets the content for the specified message structure.

        :param message_structure: The type of content to set.
        :param message: The content to set.
        :return: None
        """
        self.content[message_structure] = message

    def set_attributes(self, field: str, value: dict):
        """Sets the attributes for the specified field.

        :param field: The field to set the attributes for.
        :param value: The attributes to set.
        :return: None
        """
        if field not in self.attributes:
            self.attributes[field] = value
        else:
            self.attributes[field].update(value)

    def set_data(self, field: str, value: dict):
        """Sets the data in push notification attributes.

        :param field: The field to set the data for.
        :param value: The data to set.
        :return: None
        """
        if field not in self.data:
            self.data[field] = value
        else:
            self.data[field].update(value)

    @celery.task(bind=True)
    def send_message(self, service: str, kwargs):
        """Sends a message using the specified service driver.

        :param service: The type of service to use, such as "sns".
        :param kwargs: The keyword arguments to pass to the service
            driver.
        :return: None
        """
        driver = get_driver(service)
        driver.send(kwargs)

    def send(self):
        """Sends the message using the specified service driver.

        :return: None
        """
        kwargs = {
            "topic_arn": self.topic_arn,
            "target_arn": self.target_arn,
            "phone_number": self.phone_number,
            "subject": self.subject,
            "message_structure": self.message_structure,
            "message": json.dumps(self.message_payloads(self.message)),
            "attributes": self.attributes,
            "message_deduplication_id": self.message_deduplication_id,
            "message_group_id": self.message_group_id,
        }
        if self.run_asynk_task:
            check_required_error_message = "{} is required when run_asynk_task is set to True"
            celery_required_fields = ["CELERY_RESULT_BACKEND", "CELERY_BROKER_URL"]
            celery_response = check_required_attributes(
                celery_required_fields, check_required_error_message
            )
            if celery_response:
                self.send_message.delay(self.service, kwargs)  # pylint: disable=no-member
        else:
            self.send_message(self.service, kwargs)
