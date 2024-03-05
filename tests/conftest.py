import os

import toml

from mallow_notifications.base.logger import get_logger

logging = get_logger(__name__)


def create_test_toml_file():
    data = {}

    with open("test.toml", "w") as f:
        toml.dump(data, f)


def delete_test_toml_file():
    try:
        os.remove("test.toml")
    except FileNotFoundError:
        logging.warning("Something Went Wrong, while deleting the file")
