import json
import os
from datetime import date
import tests.bin.config as config
import yaml

import main

import pytest

OUTPUT_REPORT_DIRECTORY = os.environ.get("OUTPUT_DIR")
OUTPUT_REPORT_FILE = OUTPUT_REPORT_DIRECTORY + "/report-" + str(date.today()) + ".yaml"

RESOURCES_FILE = os.environ.get("RESOURCES_FILE")
CONFIG_FILE = os.environ.get("CONFIG_FILE")
DEFAULTS_FILE = os.environ.get("DEFAULTS_FILE")

BACKUP_RESOURCES_FILE = RESOURCES_FILE.replace(".json", ".bak.json")
BACKUP_CONFIG_FILE = CONFIG_FILE.replace(".json", ".bak.json")
BACKUP_DEFAULTS_FILE = DEFAULTS_FILE.replace(".json", ".bak.json")


@pytest.fixture(autouse=True)
def my_fixture():
    """
    Wrapper for config unit tests to back up and restore configuration to test field manipulation.
    :return:
    """
    config.backup()
    yield
    config.restore()

def test_default_setting_user():
    """
    Test generating resources with Swagger
    :return: True/False
    """

    main.main()

    # Load config
    with open(os.environ.get("CONFIG_FILE"), "r", encoding="UTF-8") as config_file:
        try:
            config_yaml = yaml.safe_load(config_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load CONFIG_FILE: %s", error_message)

    # Load output_report_file
    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report_yaml = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load CONFIG_FILE: %s", error_message)

    resource_list = list(output_report_yaml[config_yaml["swagger_resource_type"]].keys())
    if "/api/user/add" in resource_list and "/api/user" in resource_list:
        assert True
    else:
        assert False


# Test changing default on Swagger

# Test changing override on Swagger

# Test Swagger to system

# Test Swagger to containers

# Test Swagger to Database (Should fail)
