import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock

from faker import Faker

from mallow_notifications.base.utils import generate_random_arn
from mallow_notifications.sns.notification import (
    NotificationError,
    SendPushNotification,
    SendSMS,
    SendTopicMessage,
)


class TestBaseSNS(unittest.TestCase):
    def setUp(self):
        self.push = SendPushNotification()
        self.sms = SendSMS()
        self.topic = SendTopicMessage()
        self.sms.publish.client = MagicMock()
        self.topic.publish.client = MagicMock()
        self.faker = Faker()


class TestSendSMS(TestBaseSNS):
    def test_send_success_response(self):
        with mock.patch(
            "mallow_notifications.sns.endpoints.sms_sanbox.SNSSandboxSMS.get_sms_sandbox_account_status"
        ) as mock_get_sms_sandbox_account_status:
            with mock.patch(
                "mallow_notifications.sns.endpoints.sms_sanbox.SNSSandboxSMS.list_sms_sandbox_phone_numbers"
            ) as mock_list_sms_sandbox_phone_numbers:
                with mock.patch(
                    "mallow_notifications.sns.notification.SNS._send_message"
                ) as mock_send_message:
                    with mock.patch(
                        "mallow_notifications.sns.endpoints.publish.SNSPublishMessage.publish"
                    ) as mock_publish:
                        phone_number = self.faker.phone_number()

                        kwargs = {
                            "phone_number": self.faker.phone_number(),
                            "message": self.faker.pystr(min_chars=1, max_chars=180),
                        }
                        mock_get_sms_sandbox_account_status.return_value = {"IsInSandbox": True}

                        mock_list_sms_sandbox_phone_numbers.return_value = {
                            "PhoneNumbers": [
                                {
                                    "PhoneNumber": phone_number,
                                    "Status": "Verified",
                                }
                            ]
                        }

                        list_sms_numbers = mock_list_sms_sandbox_phone_numbers.return_value

                        self.sms._check_number_status(
                            list_sms_numbers["PhoneNumbers"], phone_number
                        )

                        mock_publish.return_value = {"MessageId": self.faker.pystr()}

                        mock_send_message.return_value = {"MessageId": self.faker.pystr()}
                        self.sms.send(kwargs)

                        mock_get_sms_sandbox_account_status.assert_called_once()
                        mock_list_sms_sandbox_phone_numbers.assert_called_once()
                        mock_send_message.assert_called_once()

    def test_send_with_un_verified_number(self):
        with mock.patch(
            "mallow_notifications.sns.endpoints.sms_sanbox.SNSSandboxSMS.get_sms_sandbox_account_status"
        ) as mock_get_sms_sandbox_account_status:
            with mock.patch(
                "mallow_notifications.sns.endpoints.sms_sanbox.SNSSandboxSMS.list_sms_sandbox_phone_numbers"
            ) as mock_list_sms_sandbox_phone_numbers:
                with mock.patch(
                    "mallow_notifications.sns.notification.SNS._send_message"
                ) as mock_send_message:
                    with self.assertRaises(NotificationError):
                        phone_number = self.faker.phone_number()

                        kwargs = {
                            "phone_number": phone_number,
                            "message": self.faker.pystr(min_chars=1, max_chars=180),
                        }
                        mock_get_sms_sandbox_account_status.return_value = {"IsInSandbox": True}

                        mock_list_sms_sandbox_phone_numbers.return_value = {
                            "PhoneNumbers": [
                                {
                                    "PhoneNumber": phone_number,
                                    "Status": "Pending",
                                }
                            ]
                        }

                        list_sms_numbers = mock_list_sms_sandbox_phone_numbers.return_value

                        self.sms._check_number_status(
                            list_sms_numbers["PhoneNumbers"], phone_number
                        )

                        self.sms.send(kwargs)
                        mock_get_sms_sandbox_account_status.assert_called_once()
                        mock_list_sms_sandbox_phone_numbers.assert_called_once()
                        mock_send_message.assert_not_called()

    def test_send_without_sandbox(self):
        with mock.patch(
            "mallow_notifications.sns.endpoints.sms_sanbox.SNSSandboxSMS.get_sms_sandbox_account_status"
        ) as mock_get_sms_sandbox_account_status:
            with mock.patch(
                "mallow_notifications.sns.endpoints.sms_sanbox.SNSSandboxSMS.list_sms_sandbox_phone_numbers"
            ) as mock_list_sms_sandbox_phone_numbers:
                with mock.patch(
                    "mallow_notifications.sns.notification.SNS._send_message"
                ) as mock_send_message:
                    with mock.patch(
                        "mallow_notifications.sns.endpoints.publish.SNSPublishMessage.publish"
                    ) as mock_publish:
                        phone_number = self.faker.phone_number()

                        kwargs = {
                            "phone_number": phone_number,
                            "message": self.faker.pystr(min_chars=1, max_chars=180),
                        }
                        mock_get_sms_sandbox_account_status.return_value = {"IsInSandbox": False}

                        mock_publish.return_value = {"MessageId": self.faker.pystr()}

                        mock_send_message.return_value = {"MessageId": self.faker.pystr()}
                        self.sms.send(kwargs)

                        mock_get_sms_sandbox_account_status.assert_called_once()
                        mock_list_sms_sandbox_phone_numbers.assert_not_called()
                        mock_send_message.assert_called_once()


class TestSendTopicMessage(TestBaseSNS):
    def test_send_success_response(self):
        with mock.patch(
            "mallow_notifications.sns.notification.SNS._send_message"
        ) as mock_send_message:
            with mock.patch(
                "mallow_notifications.sns.endpoints.publish.SNSPublishMessage.publish"
            ) as mock_publish:
                kwargs = {
                    "topic_arn": self.faker.uuid4(),
                    "message": self.faker.pystr(min_chars=1, max_chars=180),
                }

                mock_publish.return_value = {"MessageId": self.faker.pystr()}

                mock_send_message.return_value = {"MessageId": self.faker.pystr()}

                self.topic.send(kwargs)
                mock_send_message.assert_called_once_with(self.topic.publish, kwargs)

    def test_send_error_response(self):
        mock_error = Mock(side_effect=Exception("Error"))
        with mock.patch(
            "mallow_notifications.sns.notification.SNS._send_message", mock_error
        ) as mock_send_message:
            with self.assertRaises(NotificationError):
                self.topic.send(mock.ANY)
                mock_send_message.assert_called_once()


class TestSendPushNotification(TestBaseSNS):
    def test_send_success_response(self):
        with mock.patch(
            "mallow_notifications.sns.endpoints.push_notification.SNSPushNotification.get_endpoint_attributes"
        ) as mock_get_endpoint:
            with mock.patch(
                "mallow_notifications.sns.notification.SNS._send_message"
            ) as mock_send_message:
                with mock.patch(
                    "mallow_notifications.sns.endpoints.publish.SNSPublishMessage.publish"
                ) as mock_publish:

                    kwargs = {
                        "target_arn": generate_random_arn(
                            self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                        ),
                        "message": self.faker.pystr(min_chars=1, max_chars=180),
                        "title": self.faker.pystr(min_chars=1, max_chars=100),
                    }

                    mock_get_endpoint.return_value = {"Attributes": {"Enabled": True}}

                    mock_publish.return_value = {"MessageId": self.faker.pystr()}

                    mock_send_message.return_value = {"MessageId": self.faker.pystr()}
                    self.push.send(kwargs)

                    mock_get_endpoint.assert_called_once()
                    mock_send_message.assert_called_once_with(self.push.publish, kwargs)

    def test_send_with_device_token(self):
        with mock.patch(
            "mallow_notifications.sns.endpoints.push_notification.SNSPushNotification.get_endpoint_attributes"
        ) as mock_get_endpoint:
            with mock.patch(
                "mallow_notifications.sns.endpoints.push_notification.SNSPushNotification.create_platform_endpoint"
            ) as mock_create_endpoint:
                with mock.patch(
                    "mallow_notifications.sns.notification.SNS._send_message"
                ) as mock_send_message:
                    with mock.patch(
                        "mallow_notifications.sns.endpoints.publish.SNSPublishMessage.publish"
                    ) as mock_publish:

                        kwargs = {
                            "platform_application_arn": generate_random_arn(
                                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                            ),
                            "device_token": self.faker.pystr(min_chars=1, max_chars=180),
                            "message": self.faker.pystr(min_chars=1, max_chars=180),
                            "title": self.faker.pystr(min_chars=1, max_chars=100),
                        }

                        mock_create_endpoint.return_value = {
                            "EndpointArn": generate_random_arn(
                                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                            )
                        }

                        res = self.push._register_device(kwargs)
                        mock_get_endpoint.return_value = {"Attributes": {"Enabled": True}}

                        mock_publish.return_value = {"MessageId": self.faker.pystr()}

                        mock_send_message.return_value = {"MessageId": self.faker.pystr()}
                        self.push.send(kwargs)

                        mock_get_endpoint.assert_called_once()
                        mock_send_message.assert_called_once_with(self.push.publish, kwargs)

    def test_send_with_invalid_device_token(self):
        with mock.patch(
            "mallow_notifications.sns.endpoints.push_notification.SNSPushNotification.get_endpoint_attributes"
        ) as mock_get_endpoint:
            with mock.patch(
                "mallow_notifications.sns.endpoints.push_notification.SNSPushNotification.create_platform_endpoint"
            ) as mock_create_endpoint:
                with mock.patch(
                    "mallow_notifications.sns.endpoints.push_notification.SNSPushNotification.delete_platform_endpoint"
                ) as mock_delete_endpoint:
                    with mock.patch(
                        "mallow_notifications.sns.notification.SNS._send_message"
                    ) as mock_send_message:
                        with mock.patch(
                            "mallow_notifications.sns.endpoints.publish.SNSPublishMessage.publish"
                        ) as mock_publish:

                            kwargs = {
                                "platform_application_arn": generate_random_arn(
                                    self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                                ),
                                "device_token": self.faker.pystr(min_chars=1, max_chars=180),
                                "message": self.faker.pystr(min_chars=1, max_chars=180),
                                "title": self.faker.pystr(min_chars=1, max_chars=100),
                            }

                            mock_create_endpoint.return_value = {
                                "EndpointArn": generate_random_arn(
                                    self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                                )
                            }

                            self.push._register_device(kwargs)
                            mock_get_endpoint.return_value = {
                                "Attributes": {"Enabled": "false", "Token": kwargs["device_token"]}
                            }

                            kwargs["target_arn"] = generate_random_arn(
                                self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                            )

                            mock_delete_endpoint.return_value = None
                            token = self.push._deregister_device(kwargs, kwargs["device_token"])

                            mock_publish.return_value = {"MessageId": self.faker.pystr()}

                            mock_send_message.return_value = {"MessageId": self.faker.pystr()}

                            kwargs["target_arn"] = token

                            self.push.send(kwargs)

                            mock_get_endpoint.assert_called_once()
                            mock_send_message.assert_called_once_with(self.push.publish, kwargs)

    def test_send_error_response(self):
        with mock.patch(
            "mallow_notifications.sns.endpoints.push_notification.SNSPushNotification.get_endpoint_attributes"
        ) as mock_get_endpoint:
            with mock.patch(
                "mallow_notifications.sns.endpoints.push_notification.SNSPushNotification.create_platform_endpoint"
            ) as mock_create_endpoint:
                with mock.patch(
                    "mallow_notifications.sns.endpoints.push_notification.SNSPushNotification.delete_platform_endpoint"
                ) as mock_delete_endpoint:
                    with mock.patch(
                        "mallow_notifications.sns.notification.SNS._send_message"
                    ) as mock_send_message:
                        with mock.patch(
                            "mallow_notifications.sns.endpoints.publish.SNSPublishMessage.publish"
                        ) as mock_publish:
                            with self.assertRaises(NotificationError):

                                kwargs = {
                                    "platform_application_arn": generate_random_arn(
                                        self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                                    ),
                                    "device_token": self.faker.pystr(min_chars=1, max_chars=180),
                                    "message": self.faker.pystr(min_chars=1, max_chars=180),
                                    "title": self.faker.pystr(min_chars=1, max_chars=100),
                                }

                                mock_create_endpoint.return_value = {
                                    "EndpointArn": generate_random_arn(
                                        self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                                    )
                                }

                                self.push._register_device(kwargs)
                                mock_get_endpoint.return_value = {
                                    "Attributes": {"Enabled": "false"}
                                }

                                kwargs["target_arn"] = generate_random_arn(
                                    self.faker, self.faker.pystr(min_chars=1, max_chars=180)
                                )

                                mock_delete_endpoint.return_value = None
                                token = self.push._deregister_device(
                                    kwargs, kwargs["device_token"]
                                )

                                mock_publish.return_value = {"MessageId": self.faker.pystr()}

                                mock_send_message.return_value = {"MessageId": self.faker.pystr()}

                                kwargs["target_arn"] = token

                                self.push.send(kwargs)

                                mock_get_endpoint.assert_called_once()
                                mock_send_message.assert_called_once_with(
                                    self.push.publish, kwargs
                                )


class TestSendMessage(TestBaseSNS):
    def test_send_message(self):
        with mock.patch(
            "mallow_notifications.sns.endpoints.publish.SNSPublishMessage.publish"
        ) as mock_publish:
            kwargs = {
                "topic_arn": self.faker.uuid4(),
                "message": self.faker.pystr(min_chars=1, max_chars=180),
            }
            mock_publish.return_value = {"MessageId": self.faker.pystr()}
            self.topic._send_message(self.topic.publish, kwargs)
