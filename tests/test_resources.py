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

OUTPUT_REPORT_DIRECTORY = os.environ.get("OUTPUT_DIR")
OUTPUT_REPORT_FILE = OUTPUT_REPORT_DIRECTORY + "/report-" + str(date.today()) + ".yaml"

RESOURCES_FILE = "tests/docs/test_resources.yaml"
CONFIG_FILE = "tests/docs/test_config.yaml"
DEFAULTS_FILE = "docs/defaults.yaml"
OUTPUT_DIR = "tests/reports"
SECURITY_CHECKS_FILE = "docs/security_checks.yaml"
SWAGGER_FILE = "docs/swagger.json"

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
    Test modifying default settings for all users, verify that the generated configuration contains
    the change after creating a user.
    :return: True/False
    """

    defaults_input = config.update_default_value("users", "company_user", False)

    tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
OUTPUT_DIR,        swagger_input,
    )

    # Load defaults
    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load DEFAULTS_FILE: %s", error_message)

    if not output_report["users"]["test_user"]["company_user"]:
        assert True
    else:
        assert False


def test_override_setting_user():
    """
    Test modifying a single settings for one user, verify that the generated configuration contains
    the change for only one user after creating two.
    :return:
    """

    new_resource = {
        "name": "test_user2",
        "network": "home_network",
        "description": "Testing user2",
        "config": {"company_user": False},
    }

    resources_input = config.update_resources("users", new_resource)
    tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
OUTPUT_DIR,        swagger_input,
    )

    # Load defaults
    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load DEFAULTS_FILE: %s", error_message)

    if (
        not output_report["users"]["test_user2"]["company_user"]
        and output_report["users"]["test_user"]["company_user"]
    ):
        assert True
    else:
        assert False


def test_default_setting_networks():
    """
    Test modifying default settings for all networks, verify that the generated configuration contains
    the change after creating a network.
    :return: True/False
    """

    defaults_input = config.update_default_value("networks", "has_wifi", True)

    tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
OUTPUT_DIR,        swagger_input,
    )

    # Load defaults
    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load DEFAULTS_FILE: %s", error_message)

    if output_report["networks"]["office_network"]["has_wifi"]:
        assert True
    else:
        assert False


def test_override_setting_network():
    """
    Test modifying a single settings for one network, verify that the generated configuration
    contains the change for only one network after creating two.
    :return:
    """

    new_resource = {"name": "test_network_2", "config": {"has_wifi": True}}

    resources_input = config.update_resources("networks", new_resource)
    print(resources_input)
    tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
OUTPUT_DIR,        swagger_input,
    )

    # Load defaults
    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load DEFAULTS_FILE: %s", error_message)

    if (
        not output_report["networks"]["home_network"]["has_wifi"]
        and output_report["networks"]["test_network_2"]["has_wifi"]
    ):
        assert True
    else:
        assert False


def test_default_setting_databases():
    """
    Test modifying default settings for all databases, verify that the generated configuration contains
    the change after creating a database.
    :return: True/False
    """

    defaults_input = config.update_default_value("databases", "databases", True)

    tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
OUTPUT_DIR,        swagger_input,
    )

    # Load defaults
    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load DEFAULTS_FILE: %s", error_message)

    if output_report["databases"]["test_database"]["is_encrypted"]:
        assert True
    else:
        assert False


def test_override_setting_database():
    """
    Test modifying a single settings for one databaes, verify that the generated configuration
    contains the change for only one database after creating two.
    :return:
    """

    new_resource = {
        "name": "test_database2",
        "network": "home_network",
        "description": "Testing database2",
        "config": {"is_encrypted": False},
    }

    resources_input = config.update_resources("databases", new_resource)
    print(resources_input)
    tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
OUTPUT_DIR,        swagger_input,
    )

    # Load defaults
    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load DEFAULTS_FILE: %s", error_message)

    if (
        output_report["databases"]["test_database"]["is_encrypted"]
        and not output_report["databases"]["test_database2"]["is_encrypted"]
    ):
        assert True
    else:
        assert False


def test_default_setting_systems():
    """
    Test modifying default settings for all systems, verify that the generated configuration contains
    the change after creating a system.
    :return: True/False
    """

    defaults_input = config.update_default_value("systems", "is_hardened", False)

    tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
OUTPUT_DIR,        swagger_input,
    )

    # Load defaults
    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load DEFAULTS_FILE: %s", error_message)

    if not output_report["systems"]["test_system"]["is_hardened"]:
        assert True
    else:
        assert False


def test_override_setting_system():
    """
    Test modifying a single settings for one system, verify that the generated configuration
    contains the change for only one system after creating two.
    :return:
    """

    new_resource = {
        "name": "test_system2",
        "network": "home_network",
        "description": "Test System2",
        "config": {"is_hardened": False},
    }

    resources_input = config.update_resources("systems", new_resource)

    tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
OUTPUT_DIR,        swagger_input,
    )

    # Load defaults
    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load DEFAULTS_FILE: %s", error_message)

    if (
        output_report["systems"]["test_system"]["is_hardened"]
        and not output_report["systems"]["test_system2"]["is_hardened"]
    ):
        assert True
    else:
        assert False
