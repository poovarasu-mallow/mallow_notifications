import unittest
from unittest import mock

from faker import Faker

from mallow_notifications.base.exceptions import NotificationError
from mallow_notifications.base.utils import (
    Settings,
    check_required_attributes,
    generate_random_arn,
    handle_validation_error,
    read_file_data,
)
from tests.conftest import create_test_toml_file, delete_test_toml_file


class BaseUtils(unittest.TestCase):
    def setUp(self):
        self.faker = Faker()
        self.create_toml_file = create_test_toml_file()
        self.settings = Settings(MAIL_DRIVER=None, AWS_REGION=None)

    def tearDown(self) -> None:
        self.delete_test_toml_file = delete_test_toml_file()


class TestUtils(BaseUtils):
    def test_read_file_data_toml(self):
        with mock.patch("mallow_notifications.base.utils.toml.load") as mock_load:
            mock_load.return_value = {"key": "value"}
            data = read_file_data("test.toml")
            mock_load.assert_called_once_with(mock.ANY)
            self.assertEqual(data, {"key": "value"})

    def test_generate_random_arn(self):
        arn_value = self.faker.pystr(min_chars=1, max_chars=180)
        topic_name = self.faker.pystr(min_chars=1, max_chars=180)
        expected_response = f"arn:aws:sns:us-east-1:{arn_value}:{topic_name}"
        faker = mock.MagicMock()
        faker.random_number.return_value = arn_value
        arn = generate_random_arn(faker, topic_name)
        self.assertEqual(arn, expected_response)

    def test_handle_validation_error(self):
        field = self.faker.pystr(min_chars=1, max_chars=180)
        msg = self.faker.pystr(min_chars=1, max_chars=180)
        errors = mock.MagicMock()
        errors.errors.return_value = [{"loc": [field], "msg": msg}]
        expected_response = [f"Validation error in Field '{field}' - {msg}"]
        with self.assertRaises(NotificationError):
            response = handle_validation_error(errors)
            self.assertEqual(response, expected_response)

    def test_check_required_attributes(self):
        env_random_value = self.faker.random_element(self.settings)

        required_fields = [list(env_random_value)[0]]
        with self.assertRaises(NotificationError) as context:
            check_required_attributes(required_fields, "Missing fields: {}")
        self.assertEqual(str(context.exception), f"Missing fields: {required_fields[0]}")
