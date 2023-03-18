import json
import os
from datetime import date
import logging
import main
import tests.bin.config as config
import yaml

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

@pytest.fixture(autouse=True)
def my_fixture():
    """
    Wrapper for config unit tests to back up and restore configuration to test field manipulation.
    :return:
    """
    config.backup()
    yield
    config.restore()


def test_config_good(caplog):
    caplog.set_level(logging.ERROR)
    main.main()

    if len(caplog.records) > 0:
        assert False

    assert True


def test_config_no_title(caplog):
    caplog.set_level(logging.ERROR)

    config.delete_config("title")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        (
                "root",
                logging.ERROR,
                "\'title\'",
        ),
        (
            "root",
            logging.ERROR,
            "Config validation failed!",
        )
    ]


def test_config_no_description(caplog):
    caplog.set_level(logging.ERROR)

    config.delete_config("description")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "\'description\'",
        ),
        (
            "root",
            logging.ERROR,
            "Config validation failed!",
        )
    ]

def test_config_no_swagger_resource_type(caplog):
    caplog.set_level(logging.ERROR)

    config.delete_config("swagger_resource_type")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "\'swagger_resource_type\'",
        ),
        (
            "root",
            logging.ERROR,
            "Config validation failed!",
        )
    ]


def test_config_no_swagger_default_network(caplog):
    caplog.set_level(logging.ERROR)

    config.delete_config("swagger_default_network")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "\'swagger_default_network\'",
        ),
        (
            "root",
            logging.ERROR,
            "Config validation failed!",
        )
    ]


def test_resources_top_level_networks_missing(caplog):
    caplog.set_level(logging.ERROR)

    config.delete_resource("networks")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()
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

    config.delete_resource("users")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()
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

    config.delete_resource("databases")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()
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

    config.delete_resource("systems")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()
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

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["networks"][0]["name"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

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

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["users"][0]["name"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for user (Required: name, network, description): {'network': 'test_network', 'description': 'Testing user'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]

def test_resources_user_network(caplog):
    caplog.set_level(logging.ERROR)

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["users"][0]["network"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for user (Required: name, network, description): {'name': 'test_user', 'description': 'Testing user'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_user_description(caplog):
    caplog.set_level(logging.ERROR)

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["users"][0]["description"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for user (Required: name, network, description): {'name': 'test_user', 'network': 'test_network'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_database_description(caplog):
    caplog.set_level(logging.ERROR)

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["databases"][0]["description"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for database (Required: name, network, description): {'name': 'test_database', 'network': 'test_network'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_database_name(caplog):
    caplog.set_level(logging.ERROR)

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["databases"][0]["name"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for database (Required: name, network, description): {'network': 'test_network', 'description': 'Testing database'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]

def test_resources_database_network(caplog):
    caplog.set_level(logging.ERROR)

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["databases"][0]["network"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for database (Required: name, network, description): {'name': 'test_database', 'description': 'Testing database'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_system_name(caplog):
    caplog.set_level(logging.ERROR)

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["systems"][0]["name"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for system (Required: name, network, description): {'network': 'test_network', 'description': 'Test System'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_system_network(caplog):
    caplog.set_level(logging.ERROR)

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["systems"][0]["network"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for system (Required: name, network, description): {'name': 'test_system', 'description': 'Test System'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_system_description(caplog):
    caplog.set_level(logging.ERROR)

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["systems"][0]["description"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for system (Required: name, network, description): {'name': 'test_system', 'network': 'test_network'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_res_link_description(caplog):
    caplog.set_level(logging.ERROR)

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["res_links"][0]["description"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for res_link (Required: source, destination, description): {'source': 'test_user', 'destination': 'test_system'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]

def test_resources_res_link_source(caplog):
    caplog.set_level(logging.ERROR)

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["res_links"][0]["source"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for res_link (Required: source, destination, description): {'destination': 'test_system', 'description': 'Test connection from user to system'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_resources_res_link_destination(caplog):
    caplog.set_level(logging.ERROR)

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["res_links"][0]["destination"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        (
            "root",
            logging.ERROR,
            "Required field not set for res_link (Required: source, destination, description): {'source': 'test_user', 'description': 'Test connection from user to system'}",
        ),
        ("root", logging.ERROR, "Resources validation failed!"),
    ]


def test_defaults_top_level_systems_missing(caplog):
    caplog.set_level(logging.ERROR)

    with open(DEFAULTS_FILE, "r+", encoding="UTF-8") as defaults_file_update:
        defaults_file_update_data = json.load(defaults_file_update)
        del defaults_file_update_data["systems"]
        defaults_file_update.seek(0)
        defaults_file_update.write(json.dumps(defaults_file_update_data))
        defaults_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        ("root", logging.ERROR, "systems not found in defaults"),
        ("root", logging.ERROR, "Defaults validation failed!"),
    ]


def test_defaults_top_level_users_missing(caplog):
    caplog.set_level(logging.ERROR)

    with open(DEFAULTS_FILE, "r+", encoding="UTF-8") as defaults_file_update:
        defaults_file_update_data = json.load(defaults_file_update)
        del defaults_file_update_data["users"]
        defaults_file_update.seek(0)
        defaults_file_update.write(json.dumps(defaults_file_update_data))
        defaults_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        ("root", logging.ERROR, "users not found in defaults"),
        ("root", logging.ERROR, "Defaults validation failed!"),
    ]


def test_defaults_top_level_databases_missing(caplog):
    caplog.set_level(logging.ERROR)

    with open(DEFAULTS_FILE, "r+", encoding="UTF-8") as defaults_file_update:
        defaults_file_update_data = json.load(defaults_file_update)
        del defaults_file_update_data["databases"]
        defaults_file_update.seek(0)
        defaults_file_update.write(json.dumps(defaults_file_update_data))
        defaults_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        ("root", logging.ERROR, "databases not found in defaults"),
        ("root", logging.ERROR, "Defaults validation failed!"),
    ]


def test_defaults_top_level_networks_missing(caplog):
    caplog.set_level(logging.ERROR)

    with open(DEFAULTS_FILE, "r+", encoding="UTF-8") as defaults_file_update:
        defaults_file_update_data = json.load(defaults_file_update)
        del defaults_file_update_data["networks"]
        defaults_file_update.seek(0)
        defaults_file_update.write(json.dumps(defaults_file_update_data))
        defaults_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        ("root", logging.ERROR, "networks not found in defaults"),
        ("root", logging.ERROR, "Defaults validation failed!"),
    ]


def test_swagger_no_paths(caplog):
    caplog.set_level(logging.ERROR)

    with open(SWAGGER_FILE, "r+", encoding="UTF-8") as swagger_file_update:
        swagger_file_update_data = json.load(swagger_file_update)
        swagger_file_update_data["paths"] = {}
        swagger_file_update.seek(0)
        swagger_file_update.write(json.dumps(swagger_file_update_data))
        swagger_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        ("root", logging.ERROR, "No paths provided in swagger.json"),
        ("root", logging.ERROR, "Swagger validation failed!"),
    ]


def test_swagger_no_description(caplog):
    caplog.set_level(logging.ERROR)

    with open(SWAGGER_FILE, "r+", encoding="UTF-8") as swagger_file_update:
        swagger_file_update_data = json.load(swagger_file_update)
        del swagger_file_update_data["paths"]["/api/user/add"][
            str(list(swagger_json["paths"]["/api/user/add"].keys())[0])
        ]["description"]
        swagger_file_update.seek(0)
        swagger_file_update.write(json.dumps(swagger_file_update_data))
        swagger_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    assert caplog.record_tuples == [
        ("root", logging.ERROR, "description not set on swagger path /api/user/add"),
        ("root", logging.ERROR, "Swagger validation failed!"),
    ]
