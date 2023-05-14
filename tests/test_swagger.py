import json
import logging
import os
from datetime import date

import pytest
import yaml

import tests.bin.config as config
import tests.bin.dirs as dirs
import tmac
from bin import get_config as get_config

RESOURCES_FILE = "tests/docs/test_resources.yaml"
CONFIG_FILE = "tests/docs/test_config.yaml"
DEFAULTS_FILE = "docs/defaults.yaml"
OUTPUT_DIR = "tests/reports"
SECURITY_CHECKS_FILE = "docs/security_checks.yaml"
SWAGGER_FILE = "docs/swagger.json"

OUTPUT_REPORT_FILE = OUTPUT_DIR + "/report-" + str(date.today()) + ".yaml"

BACKUP_RESOURCES_FILE = RESOURCES_FILE.replace(".yaml", ".bak.yaml")
BACKUP_CONFIG_FILE = CONFIG_FILE.replace(".yaml", ".bak.yaml")
BACKUP_DEFAULTS_FILE = DEFAULTS_FILE.replace(".yaml", ".bak.yaml")

security_checks_input = get_config.security_checks(SECURITY_CHECKS_FILE)
resources_input = get_config.resources(RESOURCES_FILE)
config_input = get_config.config(CONFIG_FILE)
defaults_input = get_config.defaults(DEFAULTS_FILE)
swagger_input = get_config.swagger(SWAGGER_FILE)

@pytest.fixture(autouse=True)
def my_fixture():
    """
    Wrapper for config unit tests to back up and restore configuration to test field manipulation.
    :return:
    """
    dirs.create()
    config.backup()
    yield
    config.restore()


def test_default_setting_user():
    """
    Test generating resources with Swagger
    :return: True/False
    """

    tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input
    )

    # Load output_report_file
    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report_yaml = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load CONFIG_FILE: %s", error_message)

    resource_list = list(
        output_report_yaml[config_input["swagger_resource_type"]].keys()
    )
    print(resource_list)
    if "/api/user/add" in resource_list and "/api/user" in resource_list:
        assert True
    else:
        assert False


# Test changing default on Swagger

# Test changing override on Swagger

# Test Swagger to system

# Test Swagger to containers

# Test Swagger to Database (Should fail)
