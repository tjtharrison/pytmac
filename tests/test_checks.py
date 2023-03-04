import json
import os
import yaml
from datetime import date

from bin import resource_validator

import main

import pytest

OUTPUT_REPORT_DIRECTORY = os.environ.get("OUTPUT_DIR")
OUTPUT_REPORT_FILE = OUTPUT_REPORT_DIRECTORY + "/report-" + str(date.today()) + ".yaml"

RESOURCES_FILE = os.environ.get("RESOURCES_FILE")
CONFIG_FILE = os.environ.get("CONFIG_FILE")
DEFAULTS_FILE = os.environ.get("DEFAULTS_FILE")
SECURITY_CHECKS_FILE = os.environ.get("SECURITY_CHECKS_FILE")

BACKUP_RESOURCES_FILE = RESOURCES_FILE.replace(".yaml", ".bak.yaml")
BACKUP_CONFIG_FILE = CONFIG_FILE.replace(".yaml", ".bak.yaml")
BACKUP_DEFAULTS_FILE = DEFAULTS_FILE.replace(".yaml", ".bak.yaml")

# Load config
with open(os.environ.get("CONFIG_FILE"), "r", encoding="UTF-8") as config_file:
    try:
        config_yaml = yaml.safe_load(config_file)
    except yaml.YAMLError as error_message:
        logging.error("Failed to load CONFIG_FILE: %s", error_message)

# Load resources
with open(os.environ.get("RESOURCES_FILE"), "r", encoding="UTF-8") as resources_file:
    try:
        resources_yaml = yaml.safe_load(resources_file)
    except yaml.YAMLError as error_message:
        logging.error("Failed to load RESOURCES_FILE: %s", error_message)

# Load defaults
with open(os.environ.get("DEFAULTS_FILE"), "r", encoding="UTF-8") as defaults_file:
    try:
        defaults_yaml = yaml.safe_load(defaults_file)
    except yaml.YAMLError as error_message:
        logging.error("Failed to load DEFAULTS_FILE: %s", error_message)

# Load security checks
with open(
    os.environ.get("SECURITY_CHECKS_FILE"), "r", encoding="UTF-8"
) as security_checks_file:
    try:
        security_checks_yaml = yaml.safe_load(security_checks_file)
    except yaml.YAMLError as error_message:
        logging.error("Failed to load SECURITY_CHECKS_FILE: %s", error_message)


def backup_config():
    """
    Make a copy of the current resources so that it can be restored after manipulation
    :return: True
    """
    with open(BACKUP_RESOURCES_FILE, "w+", encoding="UTF-8") as resources_backup:
        yaml.dump(resources_yaml, resources_backup)

    with open(BACKUP_CONFIG_FILE, "w+", encoding="UTF-8") as config_backup:
        yaml.dump(config_yaml, config_backup)

    with open(BACKUP_DEFAULTS_FILE, "w+", encoding="UTF-8") as defaults_backup:
        yaml.dump(defaults_yaml, defaults_backup)

    return True


def restore_config():
    """
    Restore the backup version of the configuration to revert any field manipulation
    :return: True
    """
    with open(BACKUP_CONFIG_FILE, "r", encoding="UTF-8") as config_backup:
        try:
            backup_config_contents = yaml.safe_load(config_backup)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load BACKUP_CONFIG_FILE: %s", error_message)
        with open(CONFIG_FILE, "w+", encoding="UTF-8") as config_restore:
            yaml.dump(backup_config_contents, config_restore)

    with open(BACKUP_RESOURCES_FILE, "r", encoding="UTF-8") as resources_backup:
        try:
            backup_resources_contents = yaml.safe_load(resources_backup)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load BACKUP_RESOURCES_FILE: %s", error_message)
        with open(RESOURCES_FILE, "w+", encoding="UTF-8") as resources_restore:
            yaml.dump(backup_resources_contents, resources_restore)

    with open(BACKUP_DEFAULTS_FILE, "r", encoding="UTF-8") as defaults_backup:
        try:
            backup_defaults_contents = yaml.safe_load(defaults_backup)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load BACKUP_DEFAULTS_FILE: %s", error_message)
        with open(DEFAULTS_FILE, "w+", encoding="UTF-8") as defaults_restore:
            yaml.dump(backup_defaults_contents, defaults_restore)

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


def update_resources(resource_block, contents):
    """
    Update resources file with value
    :param resource_block: The block within resources that requires updating
    :param contents: The dictionary to append onto the existing resources
    :return:
    """

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resource_file_update:
        try:
            resources_yaml = yaml.safe_load(resource_file_update)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load RESOURCES_FILE: %s", error_message)
        resources_yaml["resources"][resource_block].append(contents)
        resource_file_update.seek(0)
        yaml.dump(resources_yaml, resource_file_update)


def test_user_owned_device():
    """
    Create insecure user and validate security check "user_owned_device"
    :return: True/False
    """

    new_resource = {
        "name": "test_user2",
        "network": "test_network",
        "description": "Testing user2",
        "config": {"company_user": True, "company_device": False},
    }

    update_resources("users", new_resource)
    main.main()

    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load OUTPUT_REPORT_FILE: %s", error_message)

    insecure_resources = resource_validator.do_check(
        output_report, security_checks_yaml["user_owned_device"]
    )

    insecure_resource_found = False
    for resource in insecure_resources:
        if (
            resource["name"] == security_checks_yaml["user_owned_device"]["name"]
            and resource["resource"] == "test_user2"
            and resource["description"]
            == security_checks_yaml["user_owned_device"]["description"]
            and resource["remediation"]
            == security_checks_yaml["user_owned_device"]["remediation"]
            and resource["severity"]
            == security_checks_yaml["user_owned_device"]["severity"]
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
    new_resource = {
        "name": "test_system",
        "network": "test_network",
        "description": "Testing system with no authentication",
        "config": {
            "requires_authentication": False,
        },
    }

    update_resources("systems", new_resource)
    main.main()

    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load OUTPUT_REPORT_FILE: %s", error_message)

    insecure_resources = resource_validator.do_check(
        output_report, security_checks_yaml["broken_access_control"]
    )

    insecure_resource_found = False
    for resource in insecure_resources:
        if (
            resource["name"] == security_checks_yaml["broken_access_control"]["name"]
            and resource["resource"] == "test_system"
            and resource["description"]
            == security_checks_yaml["broken_access_control"]["description"]
            and resource["remediation"]
            == security_checks_yaml["broken_access_control"]["remediation"]
            and resource["severity"]
            == security_checks_yaml["broken_access_control"]["severity"]
        ):
            insecure_resource_found = True
    if insecure_resource_found:
        assert True
    else:
        assert False


def test_cryptographic_failures():
    """
    Create insecure user and validate security check "cryptographic_failures"
    :return: True/False
    """

    new_resource = {
                                   "name": "test_database2",
                                   "network": "test_network",
                                   "description": "Testing database with no authentication",
                                   "config": {
                                       "authentication_required": False,
                                   },
                               }

    update_resources("databases", new_resource)
    main.main()

    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load OUTPUT_REPORT_FILE: %s", error_message)

    insecure_resources = resource_validator.do_check(
        output_report, security_checks_yaml["cryptographic_failures"]
    )

    insecure_resource_found = False
    for resource in insecure_resources:
        if (
            resource["name"]
            == security_checks_yaml["cryptographic_failures"]["name"]
            and resource["resource"] == "test_database2"
            and resource["description"]
            == security_checks_yaml["cryptographic_failures"]["description"]
            and resource["remediation"]
            == security_checks_yaml["cryptographic_failures"]["remediation"]
            and resource["severity"]
            == security_checks_yaml["cryptographic_failures"]["severity"]
        ):
            insecure_resource_found = True
    if insecure_resource_found:
        assert True
    else:
        assert False


def test_sql_injection():
    """
    Create insecure user and validate security check "sql_injection"
    :return: True/False
    """
    new_resource = {
                                   "name": "test_system2",
                                   "network": "test_network",
                                   "description": "Testing system with no input_validation",
                                   "config": {
                                       "input_sanitization": False,
                                   },
                               }

    update_resources("systems", new_resource)
    main.main()

    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load OUTPUT_REPORT_FILE: %s", error_message)

    insecure_resources = resource_validator.do_check(
        output_report, security_checks_yaml["sql_injection"]
    )

    insecure_resource_found = False
    for resource in insecure_resources:
        if (
            resource["name"] == security_checks_yaml["sql_injection"]["name"]
            and resource["resource"] == "test_system2"
            and resource["description"]
            == security_checks_yaml["sql_injection"]["description"]
            and resource["remediation"]
            == security_checks_yaml["sql_injection"]["remediation"]
            and resource["severity"]
            == security_checks_yaml["sql_injection"]["severity"]
        ):
            insecure_resource_found = True
    if insecure_resource_found:
        assert True
    else:
        assert False


def test_insecure_design():
    """
    Create insecure user and validate security check "insecure_design"
    :return: True/False
    """

    new_resource = {
                                   "name": "test_system2",
                                   "network": "test_network",
                                   "description": "Testing system with no dependabot_used",
                                   "config": {
                                       "dependabot_used": False,
                                   },
                               }

    update_resources("systems", new_resource)
    main.main()

    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load OUTPUT_REPORT_FILE: %s", error_message)

    insecure_resources = resource_validator.do_check(
        output_report, security_checks_yaml["insecure_design"]
    )

    insecure_resource_found = False
    for resource in insecure_resources:
        if (
            resource["name"] == security_checks_yaml["insecure_design"]["name"]
            and resource["resource"] == "test_system2"
            and resource["description"]
            == security_checks_yaml["insecure_design"]["description"]
            and resource["remediation"]
            == security_checks_yaml["insecure_design"]["remediation"]
            and resource["severity"]
            == security_checks_yaml["insecure_design"]["severity"]
        ):
            insecure_resource_found = True
    if insecure_resource_found:
        assert True
    else:
        assert False


def test_security_misconfig():
    """
    Create insecure user and validate security check "security_misconfig"
    :return: True/False
    """

    new_resource = {
                                   "name": "test_system2",
                                   "network": "test_network",
                                   "description": "Testing system with no automatic_updates",
                                   "config": {
                                       "automatic_updates": False,
                                   },
                               }

    update_resources("systems", new_resource)
    main.main()

    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load OUTPUT_REPORT_FILE: %s", error_message)

    insecure_resources = resource_validator.do_check(
        output_report, security_checks_yaml["security_misconfig"]
    )

    insecure_resource_found = False
    for resource in insecure_resources:
        if (
            resource["name"]
            == security_checks_yaml["security_misconfig"]["name"]
            and resource["resource"] == "test_system2"
            and resource["description"]
            == security_checks_yaml["security_misconfig"]["description"]
            and resource["remediation"]
            == security_checks_yaml["security_misconfig"]["remediation"]
            and resource["severity"]
            == security_checks_yaml["security_misconfig"]["severity"]
        ):
            insecure_resource_found = True
    if insecure_resource_found:
        assert True
    else:
        assert False


def test_auth_failures():
    """
    Create insecure user and validate security check "auth_failures"
    :return: True/False
    """

    new_resource = {
                                   "name": "test_system2",
                                   "network": "test_network",
                                   "description": "Testing system with no sessions_stored_securely",
                                   "config": {
                                       "delayed_login_failures": False,
                                   },
                               }

    update_resources("systems", new_resource)
    main.main()

    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load OUTPUT_REPORT_FILE: %s", error_message)

    insecure_resources = resource_validator.do_check(
        output_report, security_checks_yaml["auth_failures"]
    )

    insecure_resource_found = False
    for resource in insecure_resources:
        if (
            resource["name"] == security_checks_yaml["auth_failures"]["name"]
            and resource["resource"] == "test_system2"
            and resource["description"]
            == security_checks_yaml["auth_failures"]["description"]
            and resource["remediation"]
            == security_checks_yaml["auth_failures"]["remediation"]
            and resource["severity"]
            == security_checks_yaml["auth_failures"]["severity"]
        ):
            insecure_resource_found = True
    if insecure_resource_found:
        assert True
    else:
        assert False


def test_integrity_failure():
    """
    Create insecure user and validate security check "integrity_failure"
    :return: True/False
    """

    new_resource = {
                                   "name": "test_system2",
                                   "network": "test_network",
                                   "description": "Testing system with no code_scan_in_pipeline",
                                   "config": {
                                       "code_scan_in_pipeline": False,
                                   },
                               }

    update_resources("systems", new_resource)
    main.main()

    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load OUTPUT_REPORT_FILE: %s", error_message)

    insecure_resources = resource_validator.do_check(
        output_report, security_checks_yaml["integrity_failure"]
    )

    insecure_resource_found = False
    for resource in insecure_resources:
        if (
            resource["name"]
            == security_checks_yaml["integrity_failure"]["name"]
            and resource["resource"] == "test_system2"
            and resource["description"]
            == security_checks_yaml["integrity_failure"]["description"]
            and resource["remediation"]
            == security_checks_yaml["integrity_failure"]["remediation"]
            and resource["severity"]
            == security_checks_yaml["integrity_failure"]["severity"]
        ):
            insecure_resource_found = True
    if insecure_resource_found:
        assert True
    else:
        assert False


def test_logging_monitoring_failure():
    """
    Create insecure user and validate security check "logging_monitoring_failure"
    :return: True/False
    """

    new_resource =             {
                                   "name": "test_system2",
                                   "network": "test_network",
                                   "description": "Testing system with no tested_recovery_process",
                                   "config": {
                                       "tested_recovery_process": False,
                                   },
                               }

    update_resources("systems", new_resource)
    main.main()

    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load OUTPUT_REPORT_FILE: %s", error_message)

    insecure_resources = resource_validator.do_check(
        output_report, security_checks_yaml["logging_monitoring_failure"]
    )

    insecure_resource_found = False
    for resource in insecure_resources:
        if (
            resource["name"]
            == security_checks_yaml["logging_monitoring_failure"]["name"]
            and resource["resource"] == "test_system2"
            and resource["description"]
            == security_checks_yaml["logging_monitoring_failure"][
                "description"
            ]
            and resource["remediation"]
            == security_checks_yaml["logging_monitoring_failure"][
                "remediation"
            ]
            and resource["severity"]
            == security_checks_yaml["logging_monitoring_failure"]["severity"]
        ):
            insecure_resource_found = True
    if insecure_resource_found:
        assert True
    else:
        assert False


def test_ssrf():
    """
    Create insecure user and validate security check "ssrf"
    :return: True/False
    """

    new_resource =             {
                                   "name": "test_system2",
                                   "network": "test_network",
                                   "description": "Testing system with no least_privileged_network",
                                   "config": {
                                       "least_privileged_network": False,
                                   },
                               }

    update_resources("systems", new_resource)
    main.main()

    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load OUTPUT_REPORT_FILE: %s", error_message)

    insecure_resources = resource_validator.do_check(
        output_report, security_checks_yaml["ssrf"]
    )

    insecure_resource_found = False
    for resource in insecure_resources:
        if (
            resource["name"] == security_checks_yaml["ssrf"]["name"]
            and resource["resource"] == "test_system2"
            and resource["description"]
            == security_checks_yaml["ssrf"]["description"]
            and resource["remediation"]
            == security_checks_yaml["ssrf"]["remediation"]
            and resource["severity"]
            == security_checks_yaml["ssrf"]["severity"]
        ):
            insecure_resource_found = True
    if insecure_resource_found:
        assert True
    else:
        assert False


def test_spoofing_users():
    """
    Create insecure user and validate security check "spoofing_users"
    :return: True/False
    """

    new_resource = {
                                   "name": "test_system2",
                                   "network": "test_network",
                                   "description": "Testing system with no uses_mfa",
                                   "config": {
                                       "uses_mfa": False,
                                   },
                               }

    update_resources("users", new_resource)
    main.main()

    with open(OUTPUT_REPORT_FILE, "r", encoding="UTF-8") as output_report_file:
        try:
            output_report = yaml.safe_load(output_report_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load OUTPUT_REPORT_FILE: %s", error_message)

    insecure_resources = resource_validator.do_check(
        output_report, security_checks_yaml["spoofing_users"]
    )

    insecure_resource_found = False
    for resource in insecure_resources:
        if (
            resource["name"] == security_checks_yaml["spoofing_users"]["name"]
            and resource["resource"] == "test_system2"
            and resource["description"]
            == security_checks_yaml["spoofing_users"]["description"]
            and resource["remediation"]
            == security_checks_yaml["spoofing_users"]["remediation"]
            and resource["severity"]
            == security_checks_yaml["spoofing_users"]["severity"]
        ):
            insecure_resource_found = True
    if insecure_resource_found:
        assert True
    else:
        assert False
