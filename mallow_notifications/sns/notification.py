"""This module provides the `Notification` class, which is used to send
notifications using the Amazon SNS service."""

from mallow_notifications.base.exceptions import NotificationError
from mallow_notifications.base.logger import get_logger
from mallow_notifications.sns import (
    SNSPublishMessage,
    SNSPushNotification,
    SNSSandboxSMS,
    SNSTopics,
    SNSTopicSubscribe,
)

logging = get_logger(__name__)


class SNS:
    """Class for sending notifications using the Amazon SNS service."""

    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.notification = SNSPushNotification()
        self.publish = SNSPublishMessage()
        self.sms = SNSSandboxSMS()
        self.topic = SNSTopics()
        self.subscribe = SNSTopicSubscribe()

    def _send_message(self, client, kwargs):
        """Sends a message using the given client and message parameters and
        returns the response."""
        response = client.publish(kwargs)
        if "MessageId" in response:
            logging.info("Notification sent successfully")
            return response


class SendSMS(SNS):
    """Class for sending SMS messages using the Amazon SNS service."""

    def __init__(self):
        super().__init__()

    def _check_number_status(self, phone_number_list: list, phone_number: str):
        """Check the status of a given phone number in the phone_number_list.

        :param phone_number_list: A list of phone numbers.
        :param phone_number: The phone number to check.
        :return: The status of the phone number, or None if not found.
        """
        for number in phone_number_list:
            if number.get("PhoneNumber", None) == phone_number:
                return number.get("Status", None)
        return None

    def send(self, kwargs):
        """Send a message using the specified parameters.

        :param kwargs: A dictionary of parameters for the message.
        :raises NotificationError: If an error occurs while sending the
            message.
        """
        try:
            sms_sandbox_status = self.sms.get_sms_sandbox_account_status()
            sms_sandbox_status = sms_sandbox_status.get("IsInSandbox", False)
            if sms_sandbox_status:
                verified_phone_numbers = self.sms.list_sms_sandbox_phone_numbers({})
                number_status = self._check_number_status(
                    verified_phone_numbers.get("PhoneNumbers", []),
                    kwargs.get("phone_number", None),
                )

                if number_status == "Pending":
                    logging.debug(
                        "Verify your mobile number before sending the sms when you are in sandbox mode"  # pylint: disable=line-too-long
                    )
                    raise NotificationError(
                        "Verify your mobile number before sending the sms when you are in sandbox mode"  # pylint: disable=line-too-long
                    )

            self._send_message(self.publish, kwargs)
        except Exception as e:
            raise NotificationError(f"Someting Went Wrong: {str(e)}")


class SendTopicMessage(SNS):
    """Class for sending topic messages using the Amazon SNS service."""

    def __init__(self):
        super().__init__()

    def send(self, kwargs):
        """Send a message using the specified parameters.

        :param kwargs: A dictionary of parameters for the message.
        :raises NotificationError: If an error occurs while sending the
            message.
        """
        try:
            self._send_message(self.publish, kwargs)
        except Exception as e:
            raise NotificationError(f"Someting Went Wrong: {str(e)}")


class SendPushNotification(SNS):
    """Class for sending push notifications using the Amazon SNS service."""

    def __init__(self):
        super().__init__()

    def _register_device(self, kwargs):
        """Registers a device with the Amazon SNS service.

        :param kwargs: A dictionary of parameters for the device
            registration.
        :return: The ARN of the registered device.
        """
        endpoint_data = {
            "platform_application_arn": kwargs.get("platform_application_arn", None),
            "device_token": kwargs.get("device_token", None),
        }
        target_arn_response = self.notification.create_platform_endpoint(endpoint_data)
        return target_arn_response["EndpointArn"]

    def _deregister_device(self, kwargs, device_token):
        """Deregisters a device with the Amazon SNS service.

        :param kwargs: A dictionary of parameters for the device
            deregistration.
        :param device_token: The device token of the device to
            deregister.
        :return: The ARN of the deregistered device.
        """
        target_arn = {"target_arn": kwargs.get("target_arn", None)}
        self.notification.delete_platform_endpoint(target_arn)
        kwargs["device_token"] = device_token
        return self._register_device(kwargs)

    # pylint: disable=simplifiable-if-expression, singleton-comparison
    def send(self, kwargs):
        """Send a message using the specified parameters.

        :param kwargs: A dictionary of parameters for the message.
        :raises NotificationError: If an error occurs while sending the
            message.
        """
        try:
            if (kwargs.get("target_arn", None) is None) and (
                kwargs.get("device_token") is not None
            ):

                target_arn = self._register_device(kwargs)

            else:
                target_arn = kwargs.get("target_arn", None)

            response = self.notification.get_endpoint_attributes({"EndpointArn": target_arn})
            endpoint_enabled_response = response["Attributes"]
            endpoint_enabled = (
                True
                if (endpoint_enabled_response["Enabled"] == "true")
                or (endpoint_enabled_response["Enabled"] == True)
                else False
            )
            if endpoint_enabled is True:
                self._send_message(self.publish, kwargs)
            else:
                target_arn = self._deregister_device(kwargs, endpoint_enabled_response["Token"])
                kwargs["target_arn"] = target_arn
                self._send_message(self.publish, kwargs)
        except Exception as e:
            raise NotificationError(f"Someting Went Wrong: {str(e)}")
