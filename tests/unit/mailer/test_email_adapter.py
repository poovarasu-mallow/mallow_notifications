import unittest
from unittest import mock
from unittest.mock import MagicMock

from faker import Faker

from mallow_notifications.base.exceptions import MailError
from mallow_notifications.base.settings import Settings
from mallow_notifications.base.utils import check_required_attributes
from mallow_notifications.mailer.mail_adapter import EmailMessage, get_mailer


class BaseEmailAdapter(unittest.TestCase):
    def setUp(self):
        self.mail = EmailMessage()
        self.faker = Faker()
        self.setting = Settings()


class TestEmailMessage(BaseEmailAdapter):
    def test_send_success_with_asynk(self):
        with mock.patch(
            "mallow_notifications.mailer.mail_adapter.EmailMessage.send_email"
        ) as mock_send_email:
            with mock.patch(
                "mallow_notifications.base.utils.check_required_attributes"
            ) as mock_check:
                with mock.patch("mallow_notifications.base.settings.Settings") as mock_setting:

                    mock_setting.MAIL_DRIVER.return_value = "smtp"
                    self.mail.run_asynk_task = True

                    self.mail.from_ = self.faker.email()
                    self.mail.to = [self.faker.email()]
                    self.mail.subject = self.faker.pystr(min_chars=1, max_chars=180)
                    self.mail.set_content("plain", self.faker.pystr(min_chars=1, max_chars=256))
                    mock_check.return_value = True
                    if self.mail.run_asynk_task:
                        mock_check.return_value = True
                    mock_send_email.delay.return_value = MagicMock()
                    self.mail.send()

    def test_send_success_without_asynk(self):
        with mock.patch(
            "mallow_notifications.mailer.mail_adapter.EmailMessage.send_email"
        ) as mock_send_email:
            with mock.patch(
                "mallow_notifications.base.utils.check_required_attributes"
            ) as mock_check:

                self.mail.run_asynk_task = False

                self.mail.from_ = self.faker.email()
                self.mail.to = [self.faker.email()]
                self.mail.subject = self.faker.pystr(min_chars=1, max_chars=180)
                self.mail.set_content("plain", self.faker.pystr(min_chars=1, max_chars=256))
                mock_check.return_value = True
                mock_send_email.return_value = MagicMock()
                self.mail.send()

    def test_get_smtp_mailer(self):
        with mock.patch("mallow_notifications.mailer.mail_adapter.SMTPMail") as mock_get_mailer:
            mock_driver_instance = mock.Mock()
            mock_get_mailer.return_value = mock_driver_instance
            driver = get_mailer("smtp")

            self.assertEqual(driver, mock_driver_instance)

    def test_ge_amazon_ses_mailer(self):
        with mock.patch("mallow_notifications.mailer.mail_adapter.SESMail") as mock_get_mailer:
            mock_driver_instance = mock.Mock()
            mock_get_mailer.return_value = mock_driver_instance
            driver = get_mailer("ses")

            self.assertEqual(driver, mock_driver_instance)

    def test_get_log_mailer(self):
        with mock.patch("mallow_notifications.mailer.mail_adapter.LogMail") as mock_get_mailer:
            mock_driver_instance = mock.Mock()
            mock_get_mailer.return_value = mock_driver_instance
            driver = get_mailer("log")

            self.assertEqual(driver, mock_driver_instance)

    def test_get_invalid_mailer(self):
        with self.assertRaises(MailError):
            get_mailer(self.faker.pystr(min_chars=1, max_chars=10))
