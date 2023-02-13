import json
import os
from datetime import date

import main

import pytest

OUTPUT_REPORT_DIRECTORY = os.environ.get("OUTPUT_DIR")
OUTPUT_REPORT_FILE = OUTPUT_REPORT_DIRECTORY + "/report-" + str(date.today()) + ".json"

RESOURCES_FILE = os.environ.get("RESOURCES_FILE")
CONFIG_FILE = os.environ.get("CONFIG_FILE")
DEFAULTS_FILE = os.environ.get("DEFAULTS_FILE")

BACKUP_RESOURCES_FILE = RESOURCES_FILE.replace(".json", ".bak.json")
BACKUP_CONFIG_FILE = CONFIG_FILE.replace(".json", ".bak.json")
BACKUP_DEFAULTS_FILE = DEFAULTS_FILE.replace(".json", ".bak.json")

with open(os.environ.get("CONFIG_FILE"), encoding="UTF-8") as config_file_contents:
    config_json = json.loads(config_file_contents.read())

with open(
    os.environ.get("RESOURCES_FILE"), encoding="UTF-8"
) as resources_file_contents:
    resources_json = json.loads(resources_file_contents.read())

with open(os.environ.get("DEFAULTS_FILE"), encoding="UTF-8") as defaults_file_contents:
    defaults_json = json.loads(defaults_file_contents.read())


def backup_config():
    """
    Make a copy of the current resources so that it can be restored after manipulation
    :return: True
    """
    with open(BACKUP_RESOURCES_FILE, "w+", encoding="UTF-8") as resources_backup:
        resources_backup.write(json.dumps(resources_json))

    with open(BACKUP_CONFIG_FILE, "w+", encoding="UTF-8") as config_backup:
        config_backup.write(json.dumps(config_json))

    with open(BACKUP_DEFAULTS_FILE, "w+", encoding="UTF-8") as defaults_backup:
        defaults_backup.write(json.dumps(defaults_json))

    return True


def restore_config():
    """
    Restore the backup version of the configuration to revert any field manipulation
    :return: True
    """
    with open(BACKUP_CONFIG_FILE, "r", encoding="UTF-8") as config_backup:
        backup_config_contents = json.loads(config_backup.read())
        with open(CONFIG_FILE, "w+", encoding="UTF-8") as config_restore:
            config_restore.write(json.dumps(backup_config_contents))

    with open(BACKUP_RESOURCES_FILE, "r", encoding="UTF-8") as resources_backup:
        backup_resources_contents = json.loads(resources_backup.read())
        with open(RESOURCES_FILE, "w+", encoding="UTF-8") as resources_restore:
            resources_restore.write(json.dumps(backup_resources_contents))

    with open(BACKUP_DEFAULTS_FILE, "r", encoding="UTF-8") as defaults_backup:
        backup_defaults_contents = json.loads(defaults_backup.read())
        with open(DEFAULTS_FILE, "w+", encoding="UTF-8") as defaults_restore:
            defaults_restore.write(json.dumps(backup_defaults_contents))
    return True


@pytest.fixture(autouse=True)
def my_fixture():
    """
    Wrapper for config unit tests to back up and restore configuration to test field manipulation.
    :return:
    """
    backup_config()
    yield
    restore_config()


def test_default_setting_user():
    """
    Test modifying default settings for all users, verify that the generated configuration contains
    the change after creating a user.
    :return: True/False
    """

    with open(DEFAULTS_FILE, "r+", encoding="UTF-8") as default_file_update:
        default_file_update_data = json.load(default_file_update)
        default_file_update_data["users"]["company_user"] = False
        default_file_update.seek(0)
        default_file_update.write(json.dumps(default_file_update_data))
        default_file_update.truncate()

    main.main()

    with open(OUTPUT_REPORT_FILE) as output_report_file:
        output_report = json.loads(output_report_file.read())

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
    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resource_file_update:
        resource_file_update_data = json.load(resource_file_update)
        resource_file_update_data["resources"]["users"].append(
            {
                "name": "test_user2",
                "network": "test_network",
                "description": "Testing user2",
                "config": {"company_user": False},
            }
        )
        resource_file_update.seek(0)
        resource_file_update.write(json.dumps(resource_file_update_data))
        resource_file_update.truncate()

    main.main()

    with open(OUTPUT_REPORT_FILE) as output_report_file:
        output_report = json.loads(output_report_file.read())

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

    with open(DEFAULTS_FILE, "r+", encoding="UTF-8") as default_file_update:
        default_file_update_data = json.load(default_file_update)
        default_file_update_data["networks"]["has_wifi"] = True
        default_file_update.seek(0)
        default_file_update.write(json.dumps(default_file_update_data))
        default_file_update.truncate()

    main.main()

    with open(OUTPUT_REPORT_FILE) as output_report_file:
        output_report = json.loads(output_report_file.read())

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
    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resource_file_update:
        resource_file_update_data = json.load(resource_file_update)
        resource_file_update_data["resources"]["networks"].append(
            {"name": "test_network_2", "config": {"has_wifi": True}}
        )
        resource_file_update.seek(0)
        resource_file_update.write(json.dumps(resource_file_update_data))
        resource_file_update.truncate()

    main.main()

    with open(OUTPUT_REPORT_FILE) as output_report_file:
        output_report = json.loads(output_report_file.read())

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

    with open(DEFAULTS_FILE, "r+", encoding="UTF-8") as default_file_update:
        default_file_update_data = json.load(default_file_update)
        default_file_update_data["databases"]["is_encrypted"] = False
        default_file_update.seek(0)
        default_file_update.write(json.dumps(default_file_update_data))
        default_file_update.truncate()

    main.main()

    with open(OUTPUT_REPORT_FILE) as output_report_file:
        output_report = json.loads(output_report_file.read())

    if not output_report["databases"]["test_database"]["is_encrypted"]:
        assert True
    else:
        assert False


def test_override_setting_database():
    """
    Test modifying a single settings for one databaes, verify that the generated configuration
    contains the change for only one database after creating two.
    :return:
    """
    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resource_file_update:
        resource_file_update_data = json.load(resource_file_update)
        resource_file_update_data["resources"]["databases"].append(
            {
                "name": "test_database2",
                "network": "test_network",
                "description": "Testing database2",
                "config": {"is_encrypted": False},
            }
        )
        resource_file_update.seek(0)
        resource_file_update.write(json.dumps(resource_file_update_data))
        resource_file_update.truncate()

    main.main()

    with open(OUTPUT_REPORT_FILE) as output_report_file:
        output_report = json.loads(output_report_file.read())

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

    with open(DEFAULTS_FILE, "r+", encoding="UTF-8") as default_file_update:
        default_file_update_data = json.load(default_file_update)
        default_file_update_data["systems"]["is_hardened"] = False
        default_file_update.seek(0)
        default_file_update.write(json.dumps(default_file_update_data))
        default_file_update.truncate()

    main.main()

    with open(OUTPUT_REPORT_FILE) as output_report_file:
        output_report = json.loads(output_report_file.read())

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
    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resource_file_update:
        resource_file_update_data = json.load(resource_file_update)
        resource_file_update_data["resources"]["systems"].append(
            {
                "name": "test_system2",
                "network": "test_network",
                "description": "Test System2",
                "config": {"is_hardened": False},
            }
        )
        resource_file_update.seek(0)
        resource_file_update.write(json.dumps(resource_file_update_data))
        resource_file_update.truncate()

    main.main()

    with open(OUTPUT_REPORT_FILE) as output_report_file:
        output_report = json.loads(output_report_file.read())

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

    with open(DEFAULTS_FILE, "r+", encoding="UTF-8") as default_file_update:
        default_file_update_data = json.load(default_file_update)
        default_file_update_data["containers"]["is_hardened"] = False
        default_file_update.seek(0)
        default_file_update.write(json.dumps(default_file_update_data))
        default_file_update.truncate()

    main.main()

    with open(OUTPUT_REPORT_FILE) as output_report_file:
        output_report = json.loads(output_report_file.read())

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
    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resource_file_update:
        resource_file_update_data = json.load(resource_file_update)
        resource_file_update_data["resources"]["containers"].append(
            {
                "name": "test_container2",
                "network": "test_network",
                "description": "Test Container2",
                "config": {"is_hardened": False},
            }
        )
        resource_file_update.seek(0)
        resource_file_update.write(json.dumps(resource_file_update_data))
        resource_file_update.truncate()

    main.main()

    with open(OUTPUT_REPORT_FILE) as output_report_file:
        output_report = json.loads(output_report_file.read())

    if (
        output_report["containers"]["test_container"]["is_hardened"]
        and not output_report["containers"]["test_container2"]["is_hardened"]
    ):
        assert True
    else:
        assert False
