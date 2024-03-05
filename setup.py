"""This module provides the `setup` function for the `mallow_notifications`
package."""

from setuptools import find_packages, setup

from mallow_notifications.base.utils import read_file_data

poetry_toml = read_file_data("pyproject.toml")

dependencies = poetry_toml["tool"]["poetry"]["dependencies"]
dev_dependencies = poetry_toml["tool"]["poetry"]["group"]["dev"]["dependencies"]

# Combine dependencies and dev-dependencies
all_dependencies = dependencies.copy()

all_dependencies.pop("python", None)

extra_dependencies = dev_dependencies.copy()

# Extract the package names and versions
install_requires = [f"{package}=={version}" for package, version in all_dependencies.items()]
extra_install_requires = [
    f"{package}=={version}" for package, version in extra_dependencies.items()
]


setup(
    name="mallow_notifications",
    version="0.0.1",
    keywords=[
        "python",
        "notification",
        "amazon",
        "sns",
        "ses",
        "sms",
        "email",
        "push notification",
        "smtp",
    ],
    packages=find_packages(exclude=["tests*"]),
    install_requires=install_requires,
    extras_require={"dev": extra_install_requires},
    description="Library for sending notifications using the Amazon SNS service and multiple email services.",  # pylint: disable=line-too-long
    long_description=read_file_data("README.md"),
    author="Mallow Technologies, Inc.",
    author_email="poovarasu@mallow-tech.com",
    url="https://github.com/poovarasu-mallow/mallow_notifications",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        # 'License :: OSI Approved :: Apache Software License', # Licence to be add
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
