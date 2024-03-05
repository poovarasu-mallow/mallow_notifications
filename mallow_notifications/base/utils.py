"""Module for defining the utility functions used in the package."""
from typing import Optional

import toml
from faker import Faker
from pydantic import ValidationError

from mallow_notifications.base.exceptions import NotificationError
from mallow_notifications.base.settings import Settings

settings = Settings()


def read_file_data(file_path: str) -> str:
    """Read data from a file and return it as a string.

    :param file_path: a string representing the path to the file
    :type file_path: str
    :return: the content of the file as a string
    :rtype: str
    """
    extension = file_path.split(".")[1]
    with open(file_path, "r") as file:  # pylint: disable=unspecified-encoding
        return toml.load(file) if extension == "toml" else file.read()


def generate_random_arn(faker: Faker, name: str, account_id_length: Optional[int] = 12) -> str:
    """Generate a random Amazon Resource Name (ARN) for the given name and
    account ID length.

    Args:
        faker (Faker): A Faker object for generating random data.
        name (str): The name to be included in the ARN.
        account_id_length (int, optional): The length of the AWS account ID. Defaults to 12.

    Returns:
        str: The generated ARN string.
    """
    region = settings.AWS_REGION
    account_id = faker.random_number(digits=account_id_length)
    return f"arn:aws:sns:{region}:{account_id}:{name}"


def handle_validation_error(errors: ValidationError) -> None:
    """Function to handle validation errors and raise a NotificationError with
    error messages.

    :param errors: ValidationError object containing validation errors
    :type errors: ValidationError
    :return: None
    :rtype: None
    """
    error_messages = []
    for error in errors.errors():
        loc, msg = error["loc"][0], error["msg"]
        error_message = f"Validation error in Field '{loc}' - {msg}"
        error_messages.append(error_message)
    raise NotificationError(error_messages)


def check_required_attributes(required_fields: list, error_message: str) -> bool:
    """Check if the required attributes are present and raise an error if any
    are missing.

    :param required_fields: a list of required attribute names
    :param error_message: a message to be formatted with the missing
        fields
    :return: a boolean indicating if all required attributes are present
    """
    values = {field: getattr(settings, field) for field in required_fields}
    missing_fields = [field for field, value in values.items() if value is None or value == ""]

    if len(missing_fields) > 0:
        raise NotificationError(error_message.format(", ".join(missing_fields)))
    return True
