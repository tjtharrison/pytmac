import json
import os
from datetime import date

from bin import resource_validator

import main

import pytest

OUTPUT_REPORT_DIRECTORY = os.environ.get("OUTPUT_DIR")
OUTPUT_REPORT_FILE = OUTPUT_REPORT_DIRECTORY + "/report-" + str(date.today()) + ".json"

RESOURCES_FILE = os.environ.get("RESOURCES_FILE")
CONFIG_FILE = os.environ.get("CONFIG_FILE")
DEFAULTS_FILE = os.environ.get("DEFAULTS_FILE")
SECURITY_CHECKS_FILE = os.environ.get("SECURITY_CHECKS_FILE")

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

with open(
    os.environ.get("SECURITY_CHECKS_FILE"), encoding="UTF-8"
) as security_checks_file_contents:
    security_checks_file_contents = json.loads(security_checks_file_contents.read())


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


def test_user_owned_device():
    """
    Create insecure user and validate security check "user_owned_device"
    :return: True/False
    """

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resource_file_update:
        resource_file_update_data = json.load(resource_file_update)
        resource_file_update_data["resources"]["users"].append(
            {
                "name": "test_user2",
                "network": "test_network",
                "description": "Testing user2",
                "config": {"company_user": True, "company_device": False},
            }
        )
        resource_file_update.seek(0)
        resource_file_update.write(json.dumps(resource_file_update_data))
        resource_file_update.truncate()

    main.main()

    with open(OUTPUT_REPORT_FILE) as output_report_file:
        output_report = json.loads(output_report_file.read())

    insecure_resources = resource_validator.do_check(
        output_report, security_checks_file_contents["user_owned_device"]
    )

    insecure_resource_found = False
    for resource in insecure_resources:
        if (
            resource["name"]
            == security_checks_file_contents["user_owned_device"]["name"]
            and resource["resource"] == "test_user2"
            and resource["description"]
            == security_checks_file_contents["user_owned_device"]["description"]
            and resource["remediation"]
            == security_checks_file_contents["user_owned_device"]["remediation"]
            and resource["severity"]
            == security_checks_file_contents["user_owned_device"]["severity"]
        ):
            insecure_resource_found = True
    if insecure_resource_found:
        assert True
    else:
        assert False

def test_broken_access_control():
    """
    Create insecure user and validate security check "broken_access_control"
    :return: True/False
    """

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resource_file_update:
        resource_file_update_data = json.load(resource_file_update)
        resource_file_update_data["resources"]["systems"].append(
            {
                "name": "test_system",
                "network": "test_network",
                "description": "Testing system with no authentication",
                "config": {
                    "requires_authentication": False,
                },
            }
        )
        resource_file_update.seek(0)
        resource_file_update.write(json.dumps(resource_file_update_data))
        resource_file_update.truncate()

    main.main()

    with open(OUTPUT_REPORT_FILE) as output_report_file:
        output_report = json.loads(output_report_file.read())

    insecure_resources = resource_validator.do_check(
        output_report, security_checks_file_contents["broken_access_control"]
    )

    insecure_resource_found = False
    for resource in insecure_resources:
        if (
                resource["name"]
                == security_checks_file_contents["broken_access_control"]["name"]
                and resource["resource"] == "test_system"
                and resource["description"]
                == security_checks_file_contents["broken_access_control"]["description"]
                and resource["remediation"]
                == security_checks_file_contents["broken_access_control"]["remediation"]
                and resource["severity"]
                == security_checks_file_contents["broken_access_control"]["severity"]
        ):
            insecure_resource_found = True
    if insecure_resource_found:
        assert True
    else:
        assert False
