from setuptools import setup, find_packages
import os

PROJECT_NAME = "Solar-panel-inverter-logger"
PROJECT_PACKAGE_NAME = "solarInverterToHass"

PROJECT_GITHUB_USERNAME = "neotje"

PACKAGES = find_packages()

REQUIRED = [
    "paho-mqtt>=1.6.1",
    "pyserial>=3.5"
]

setup(
    name=PROJECT_PACKAGE_NAME,
    packages=PACKAGES,
    install_requires=REQUIRED,
    entry_points={"console_scripts": [
        "solarInverterToHass = solarInverterToHass.__main__:main"]}
)