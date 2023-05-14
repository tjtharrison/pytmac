import json
import os
from datetime import date
import logging
import tmac
import tests.bin.config as config
import tests.bin.dirs as dirs
from bin import get_config as get_config
import yaml

import pytest



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

# Load swagger
with open(os.environ.get("SWAGGER_FILE"), encoding="UTF-8") as swagger_file_contents:
    swagger_json = json.loads(swagger_file_contents.read())


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


def test_config_good(caplog):
    caplog.set_level(logging.ERROR)
    tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    if len(caplog.records) > 0:
        assert False

    assert True


def test_config_no_title(caplog):
    caplog.set_level(logging.ERROR)

    config_input = config.delete_config("title")
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        tmac.main(
            resources_input,
            config_input,
            defaults_input,
            security_checks_input,
            OUTPUT_DIR,
            swagger_input,
        )

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "'title'",
        ),
        (
            "root",
            logging.ERROR,
            "Config validation failed!",
        ),
    ]


def test_config_no_description(caplog):
    caplog.set_level(logging.ERROR)

    config_input = config.delete_config("description")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        tmac.main(
            resources_input,
            config_input,
            defaults_input,
            security_checks_input,
            OUTPUT_DIR,
            swagger_input,
        )

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "'description'",
        ),
        (
            "root",
            logging.ERROR,
            "Config validation failed!",
        ),
    ]


def test_config_no_swagger_resource_type(caplog):
    caplog.set_level(logging.ERROR)

    config_input = config.delete_config("swagger_resource_type")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        tmac.main(
            resources_input,
            config_input,
            defaults_input,
            security_checks_input,
            OUTPUT_DIR,
            swagger_input,
        )

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "'swagger_resource_type'",
        ),
        (
            "root",
            logging.ERROR,
            "Config validation failed!",
        ),
    ]


def test_config_no_swagger_default_network(caplog):
    caplog.set_level(logging.ERROR)

    config_input = config.delete_config("swagger_default_network")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        tmac.main(
            resources_input,
            config_input,
            defaults_input,
            security_checks_input,
            OUTPUT_DIR,
            swagger_input,
        )

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "'swagger_default_network'",
        ),
        (
            "root",
            logging.ERROR,
            "Config validation failed!",
        ),
    ]


def test_resources_top_level_networks_missing(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("networks")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        tmac.main(
            resources_input,
            config_input,
            defaults_input,
            security_checks_input,
            OUTPUT_DIR,
            swagger_input,
        )
    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "networks not found in resources",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_top_level_users_missing(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("users")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )
    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "users not found in resources",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_top_level_databases_missing(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("databases")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )
    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "databases not found in resources",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_top_level_systems_missing(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("systems")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )
    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "systems not found in resources",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_networks_name(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("networks.name")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "name not set for network: {}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_user_name(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("users.name")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for user (Required: name, network, description): {'description': 'Testing user', 'network': 'home_network'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_user_network(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("users.network")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for user (Required: name, network, description): {'description': 'Testing user', 'name': 'test_user'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_user_description(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("users.description")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for user (Required: name, network, description): {'name': 'test_user', 'network': 'home_network'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_database_description(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("databases.description")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for database (Required: name, network, description): {'name': 'test_database', 'network': 'office_network'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_database_name(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("databases.name")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for database (Required: name, network, description): {'description': 'Testing database', 'network': 'office_network'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_database_network(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("databases.network")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for database (Required: name, network, description): {'description': 'Testing database', 'name': 'test_database'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_system_name(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("systems.name")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for system (Required: name, network, description): {'description': 'Testing system', 'network': 'office_network'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_system_network(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("systems.network")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for system (Required: name, network, description): {'description': 'Testing system', 'name': 'test_system'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_system_description(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("systems.description")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for system (Required: name, network, description): {'name': 'test_system', 'network': 'office_network'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_res_link_description(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("res_links.description")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for res_link (Required: source, destination, description): {'destination': 'test_system', 'source': 'test_user'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_res_link_source(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("res_links.source")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for res_link (Required: source, destination, description): {'description': 'Test connection from user to system', 'destination': 'test_system'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_res_link_destination(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("res_links.destination")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for res_link (Required: source, destination, description): {'description': 'Test connection from user to system', 'source': 'test_user'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_defaults_top_level_systems_missing(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("systems")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    assert caplog.record_tuples == [
        ("root", logging.ERROR, "systems not found in resources"),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_defaults_top_level_users_missing(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("users")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    assert caplog.record_tuples == [
        ("root", logging.ERROR, "users not found in resources"),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_defaults_top_level_databases_missing(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("databases")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    assert caplog.record_tuples == [
        ("root", logging.ERROR, "databases not found in resources"),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_defaults_top_level_networks_missing(caplog):
    caplog.set_level(logging.ERROR)

    resources_input = config.delete_resource("networks")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    assert caplog.record_tuples == [
        ("root", logging.ERROR, "networks not found in resources"),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


# def test_swagger_no_paths(caplog):
#     caplog.set_level(logging.ERROR)
#
#     with open(SWAGGER_FILE, "r+", encoding="UTF-8") as swagger_file_update:
#         swagger_file_update_data = json.load(swagger_file_update)
#         swagger_file_update_data["paths"] = {}
#         swagger_file_update.seek(0)
#         swagger_file_update.write(json.dumps(swagger_file_update_data))
#         swagger_file_update.truncate()
#
#     with pytest.raises(SystemExit) as pytest_wrapped_e:
#             tmac.main(
#         resources_input,
#         config_input,
#         defaults_input,
#         security_checks_input,
#         OUTPUT_DIR,
#         swagger_input,
#     )
#
#     assert caplog.record_tuples == [
#         ("root", logging.ERROR, "No paths provided in swagger.json"),
#         ("root", logging.ERROR, "Swagger validation failed!"),
#     ]
#
#
# def test_swagger_no_description(caplog):
#     caplog.set_level(logging.ERROR)
#
#     with open(SWAGGER_FILE, "r+", encoding="UTF-8") as swagger_file_update:
#         swagger_file_update_data = json.load(swagger_file_update)
#         del swagger_file_update_data["paths"]["/api/user/add"][
#             str(list(swagger_json["paths"]["/api/user/add"].keys())[0])
#         ]["description"]
#         swagger_file_update.seek(0)
#         swagger_file_update.write(json.dumps(swagger_file_update_data))
#         swagger_file_update.truncate()
#
#     with pytest.raises(SystemExit) as pytest_wrapped_e:
#             tmac.main(
#         resources_input,
#         config_input,
#         defaults_input,
#         security_checks_input,
#         OUTPUT_DIR,
#         swagger_input,
#     )
#
#     assert caplog.record_tuples == [
#         ("root", logging.ERROR, "description not set on swagger path /api/user/add"),
#         ("root", logging.ERROR, "Swagger validation failed!"),
#     ]
