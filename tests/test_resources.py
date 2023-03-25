import json
import os
from datetime import date
import yaml
import main
import tests.bin.config as config
import tests.bin.dirs as dirs

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

    config.update_default_value("users", "company_user", False)

    main.main()

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
        "network": "test_network",
        "description": "Testing user2",
        "config": {"company_user": False},
    }

    config.update_resources("users", new_resource)

    main.main()

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

    config.update_default_value("networks", "has_wifi", True)

    main.main()

    # Load defaults
    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load DEFAULTS_FILE: %s", error_message)

    if output_report["networks"]["test_network"]["has_wifi"]:
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

    config.update_resources("networks", new_resource)

    main.main()

    # Load defaults
    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load DEFAULTS_FILE: %s", error_message)

    if (
        not output_report["networks"]["test_network"]["has_wifi"]
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

    config.update_default_value("databases", "databases", True)

    main.main()

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
        "network": "test_network",
        "description": "Testing database2",
        "config": {"is_encrypted": False},
    }

    config.update_resources("databases", new_resource)

    main.main()

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

    config.update_default_value("systems", "is_hardened", False)

    main.main()

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
        "network": "test_network",
        "description": "Test System2",
        "config": {"is_hardened": False},
    }

    config.update_resources("systems", new_resource)

    main.main()

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


def test_default_setting_containers():
    """
    Test modifying default settings for all containers, verify that the generated configuration contains
    the change after creating a container.
    :return: True/False
    """

    config.update_default_value("systems", "is_hardened", False)

    main.main()

    # Load defaults
    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load DEFAULTS_FILE: %s", error_message)

    if not output_report["containers"]["test_container"]["is_hardened"]:
        assert True
    else:
        assert False


def test_override_setting_containers():
    """
    Test modifying a single settings for one system, verify that the generated configuration
    contains the change for only one system after creating two.
    :return:
    """

    new_resource = {
        "name": "test_container2",
        "network": "test_network",
        "description": "Test Container2",
        "config": {"is_hardened": False},
    }

    config.update_resources("containers", new_resource)

    main.main()

    # Load defaults
    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load DEFAULTS_FILE: %s", error_message)

    if (
        output_report["containers"]["test_container"]["is_hardened"]
        and not output_report["containers"]["test_container2"]["is_hardened"]
    ):
        assert True
    else:
        assert False
