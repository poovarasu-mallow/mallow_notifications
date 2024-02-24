import unittest
from unittest import mock
from unittest.mock import MagicMock

from faker import Faker

from mallow_notifications.base.utils import generate_random_arn
from mallow_notifications.sns.notification_adpater import (
    Notification,
    NotificationError,
    get_driver,
)


class TestNotificationAdapter(unittest.TestCase):
    def setUp(self):
        self.notification = Notification()
        self.faker = Faker()

    def test_send_with_async_task(self):
        self.notification.topic_arn = generate_random_arn(
            self.faker, self.faker.pystr(min_chars=1, max_chars=180)
        )
        self.notification.subject = self.faker.pystr(min_chars=1, max_chars=180)
        self.notification.message = self.faker.pystr(min_chars=1, max_chars=256)
        self.notification.message_structure = "json"
        self.notification.set_content(
            self.notification.message_structure, self.notification.message
        )
        self.notification.run_asynk_task = True
        self.notification.service = "email"

        with mock.patch(
            "mallow_notifications.sns.notification_adpater.check_required_attributes",
            return_value=self.notification.service,
        ) as mock_check_celery_attributes:
            with mock.patch(
                "mallow_notifications.sns.notification_adpater.Notification.send_message",
                return_value=None,
            ) as mock_send_messages:
                self.notification.send()
                check_required_error_message = "{} is required when run_asynk_task is set to True"
                celery_required_fields = ["CELERY_RESULT_BACKEND", "CELERY_BROKER_URL"]
                mock_check_celery_attributes.assert_called_once_with(
                    celery_required_fields, check_required_error_message
                )
                mock_check_celery_attributes.assert_called_once()
                mock_send_messages.assert_not_called()

    def test_send_with_sync_task(self):
        self.notification.topic_arn = generate_random_arn(
            self.faker, self.faker.pystr(min_chars=1, max_chars=180)
        )
        self.notification.subject = self.faker.pystr(min_chars=1, max_chars=180)
        self.notification.message = self.faker.pystr(min_chars=1, max_chars=256)
        self.notification.message_structure = "json"
        self.notification.set_content(
            self.notification.message_structure, self.notification.message
        )
        self.notification.run_asynk_task = False
        self.notification.service = "email"

        with mock.patch(
            "mallow_notifications.sns.notification_adpater.check_required_attributes",
            return_value=self.notification.service,
        ) as mock_check_celery_attributes:
            with mock.patch(
                "mallow_notifications.sns.notification_adpater.Notification.send_message"
            ) as mock_send_messages:
                self.notification.send()
                mock_send_messages.delay.assert_not_called()

    def test_send_message(self):
        self.notification.service = "email"
        with mock.patch(
            "mallow_notifications.sns.notification_adpater.get_driver"
        ) as mock_get_driver:
            mock_get_driver.return_value = mock.Mock()
            self.notification.send_message("email", kwargs=mock.ANY)

            mock_get_driver.assert_called_once()
            mock_get_driver.assert_called_once_with(self.notification.service)

    def test_get_driver_email(self):
        with mock.patch(
            "mallow_notifications.sns.notification_adpater.SendTopicMessage"
        ) as mock_get_driver:
            mock_driver_instance = mock.Mock()
            mock_get_driver.return_value = mock_driver_instance
            driver = get_driver("email")

            self.assertEqual(driver, mock_driver_instance)

    def test_get_driver_topic(self):
        with mock.patch(
            "mallow_notifications.sns.notification_adpater.SendTopicMessage"
        ) as mock_get_driver:
            mock_driver_instance = mock.Mock()
            mock_get_driver.return_value = mock_driver_instance
            driver = get_driver("topic")

            self.assertEqual(driver, mock_driver_instance)

    def test_get_driver_push(self):
        with mock.patch(
            "mallow_notifications.sns.notification_adpater.SendPushNotification"
        ) as mock_get_driver:
            mock_driver_instance = mock.Mock()
            mock_get_driver.return_value = mock_driver_instance
            driver = get_driver("push")

            self.assertEqual(driver, mock_driver_instance)

    def test_get_driver_sms(self):
        with mock.patch(
            "mallow_notifications.sns.notification_adpater.SendSMS"
        ) as mock_get_driver:
            mock_driver_instance = mock.Mock()
            mock_get_driver.return_value = mock_driver_instance
            driver = get_driver("sms")

            self.assertEqual(driver, mock_driver_instance)

    def test_get_driver_invalid(self):
        with self.assertRaises(NotificationError):
            get_driver(self.faker.pystr(min_chars=1, max_chars=10))

    def test_get_gcm_message(self):
        self.notification.title = self.faker.pystr(min_chars=1, max_chars=100)
        self.notification.message = self.faker.pystr(min_chars=1, max_chars=256)
        self.notification.data = mock.ANY

        expected_message = "{{ notification: {{ title: {title}, text: {text}, body: {body}, sound: {sound} }}, data: {data} }}".format(
            title=self.notification.title,
            text=(
                self.notification.message
                if self.notification.gcm_message is None
                else self.notification.gcm_message
            ),
            body=(
                self.notification.message
                if self.notification.gcm_message is None
                else self.notification.gcm_message
            ),
            sound=("default" if self.notification.sound is None else self.notification.sound),
            data=self.notification.data,
        )

        gcm_messgae = self.notification._get_gcm_message(self.notification.message)

        self.assertEqual(gcm_messgae, expected_message)

    def test_apns_message_with_badge(self):
        self.notification.title = self.faker.pystr(min_chars=1, max_chars=100)
        self.notification.data = mock.ANY

        expected_message = (
            '{{ "aps": {{ "alert": {title},"sound": {sound} }}, "acme2": {data}}}'.format(
                title=self.notification.title,
                sound=("default" if self.notification.sound is None else self.notification.sound),
                data=self.notification.data,
            )
        )

        apns_messgae = self.notification._apns_message(self.notification.message)

        self.assertEqual(apns_messgae, expected_message)

    def test_apns_message_without_badge(self):
        self.notification.title = self.faker.pystr(min_chars=1, max_chars=100)
        self.notification.data = mock.ANY
        self.notification.badge = 1

        expected_message = '{{ "aps": {{ "alert": {title},"sound": {sound}, "badge": {badge}}}, "acme2": {data}}}'.format(
            title=self.notification.title,
            sound=("default" if self.notification.sound is None else self.notification.sound),
            badge=self.notification.badge,
            data=self.notification.data,
        )

        apns_messgae = self.notification._apns_message(self.notification.message)

        self.assertEqual(apns_messgae, expected_message)

    def test_set_content(self):
        key = self.faker.pystr(min_chars=1, max_chars=100)
        value = self.faker.pystr(min_chars=1, max_chars=100)
        expected_data = {key: value}
        self.notification.set_content(key, value)

        self.assertEqual(self.notification.content, expected_data)

    def test_set_attributes(self):
        key = self.faker.pystr(min_chars=1, max_chars=100)
        value = self.faker.pystr(min_chars=1, max_chars=100)
        value_dict = {key: value, value: key}
        expected_data = {key: value_dict}
        self.notification.set_attributes(key, {key: value})
        self.notification.set_attributes(key, {value: key})

        self.assertEqual(self.notification.attributes, expected_data)
