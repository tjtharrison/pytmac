import logging
import os
from datetime import date

import pytest
import yaml

import tests.bin.config as config
import tests.bin.dirs as dirs
import pytmac
from bin import get_config as get_config
from bin import resource_validator as resource_validator

RESOURCES_FILE = "tests/docs/test_resources.yaml"
CONFIG_FILE = "tests/docs/test_config.yaml"
DEFAULTS_FILE = "conf/defaults.yaml"
OUTPUT_DIR = "tests/reports"
SECURITY_CHECKS_FILE = "conf/security_checks.yaml"
SWAGGER_FILE = "conf/swagger.json"

OUTPUT_REPORT_FILE = OUTPUT_DIR + "/report-" + str(date.today()) + ".yaml"

BACKUP_RESOURCES_FILE = RESOURCES_FILE.replace(".yaml", ".bak.yaml")
BACKUP_CONFIG_FILE = CONFIG_FILE.replace(".yaml", ".bak.yaml")
BACKUP_DEFAULTS_FILE = DEFAULTS_FILE.replace(".yaml", ".bak.yaml")

security_checks_input = get_config.security_checks(SECURITY_CHECKS_FILE)
resources_input = get_config.resources(RESOURCES_FILE)
config_input = get_config.config(CONFIG_FILE)
defaults_input = get_config.defaults(DEFAULTS_FILE)
swagger_input = get_config.swagger(SWAGGER_FILE)

# Load security checks
with open(
    SECURITY_CHECKS_FILE, "r", encoding="UTF-8"
) as security_checks_file:
    try:
        security_checks_yaml = yaml.safe_load(security_checks_file)
    except yaml.YAMLError as error_message:
        logging.error("Failed to load SECURITY_CHECKS_FILE: %s", error_message)


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


def test_user_owned_device():
    """
    Create insecure user and validate security check "user_owned_device"
    :return: True/False
    """

    new_resource = {
        "name": "test_user2",
        "network": "home_network",
        "description": "Testing user2",
        "config": {"company_user": True, "company_device": False},
    }

    resources_input = config.update_resources("users", new_resource)
    pytmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

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
        "network": "home_network",
        "description": "Testing system with no authentication",
        "config": {
            "requires_authentication": False,
        },
    }

    resources_input = config.update_resources("systems", new_resource)
    pytmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

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
        "network": "home_network",
        "description": "Testing database with no authentication",
        "config": {
            "authentication_required": False,
        },
    }

    resources_input = config.update_resources("databases", new_resource)
    pytmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

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
            resource["name"] == security_checks_yaml["cryptographic_failures"]["name"]
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
        "network": "home_network",
        "description": "Testing system with no input_validation",
        "config": {
            "input_sanitization": False,
        },
    }

    resources_input = config.update_resources("systems", new_resource)
    pytmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

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
        "network": "home_network",
        "description": "Testing system with no dependabot_used",
        "config": {
            "dependabot_used": False,
        },
    }

    resources_input = config.update_resources("systems", new_resource)
    pytmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

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
        "network": "home_network",
        "description": "Testing system with no automatic_updates",
        "config": {
            "automatic_updates": False,
        },
    }

    resources_input = config.update_resources("systems", new_resource)
    pytmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

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
            resource["name"] == security_checks_yaml["security_misconfig"]["name"]
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
        "network": "home_network",
        "description": "Testing system with no sessions_stored_securely",
        "config": {
            "delayed_login_failures": False,
        },
    }

    resources_input = config.update_resources("systems", new_resource)
    pytmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

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
        "network": "home_network",
        "description": "Testing system with no code_scan_in_pipeline",
        "config": {
            "code_scan_in_pipeline": False,
        },
    }

    resources_input = config.update_resources("systems", new_resource)
    pytmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

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
            resource["name"] == security_checks_yaml["integrity_failure"]["name"]
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

    new_resource = {
        "name": "test_system2",
        "network": "home_network",
        "description": "Testing system with no tested_recovery_process",
        "config": {
            "tested_recovery_process": False,
        },
    }

    resources_input = config.update_resources("systems", new_resource)
    pytmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

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
            == security_checks_yaml["logging_monitoring_failure"]["description"]
            and resource["remediation"]
            == security_checks_yaml["logging_monitoring_failure"]["remediation"]
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

    new_resource = {
        "name": "test_system2",
        "network": "home_network",
        "description": "Testing system with no least_privileged_network",
        "config": {
            "least_privileged_network": False,
        },
    }

    resources_input = config.update_resources("systems", new_resource)
    pytmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

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
            and resource["description"] == security_checks_yaml["ssrf"]["description"]
            and resource["remediation"] == security_checks_yaml["ssrf"]["remediation"]
            and resource["severity"] == security_checks_yaml["ssrf"]["severity"]
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
        "network": "home_network",
        "description": "Testing system with no uses_mfa",
        "config": {
            "uses_mfa": False,
        },
    }

    resources_input = config.update_resources("users", new_resource)
    pytmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

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
