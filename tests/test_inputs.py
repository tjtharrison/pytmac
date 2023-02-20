import json
import os
from datetime import date
import logging
import main

import pytest

OUTPUT_REPORT_DIRECTORY = os.environ.get("OUTPUT_DIR")
OUTPUT_REPORT_FILE = OUTPUT_REPORT_DIRECTORY + "/report-" + str(date.today()) + ".json"

RESOURCES_FILE = os.environ.get("RESOURCES_FILE")
CONFIG_FILE = os.environ.get("CONFIG_FILE")
DEFAULTS_FILE = os.environ.get("DEFAULTS_FILE")
SWAGGER_FILE = os.environ.get("SWAGGER_FILE")

BACKUP_RESOURCES_FILE = RESOURCES_FILE.replace(".json", ".bak.json")
BACKUP_CONFIG_FILE = CONFIG_FILE.replace(".json", ".bak.json")
BACKUP_DEFAULTS_FILE = DEFAULTS_FILE.replace(".json", ".bak.json")
BACKUP_SWAGGER_FILE = SWAGGER_FILE.replace(".json", ".bak.json")

with open(os.environ.get("CONFIG_FILE"), encoding="UTF-8") as config_file_contents:
    config_json = json.loads(config_file_contents.read())

with open(
    os.environ.get("RESOURCES_FILE"), encoding="UTF-8"
) as resources_file_contents:
    resources_json = json.loads(resources_file_contents.read())

with open(os.environ.get("DEFAULTS_FILE"), encoding="UTF-8") as defaults_file_contents:
    defaults_json = json.loads(defaults_file_contents.read())

with open(os.environ.get("SWAGGER_FILE"), encoding="UTF-8") as swagger_file_contents:
    swagger_json = json.loads(swagger_file_contents.read())


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

    with open(BACKUP_SWAGGER_FILE, "w+", encoding="UTF-8") as swagger_backup:
        swagger_backup.write(json.dumps(swagger_json))

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

    with open(BACKUP_SWAGGER_FILE, "r", encoding="UTF-8") as swagger_backup:
        backup_swagger_contents = json.loads(swagger_backup.read())
        with open(SWAGGER_FILE, "w+", encoding="UTF-8") as swagger_restore:
            swagger_restore.write(json.dumps(backup_swagger_contents))

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


def test_config_good(caplog):
    caplog.set_level(logging.ERROR)
    main.main()

    if len(caplog.records) > 0:
        assert False

    assert True


def test_config_no_title(caplog):
    caplog.set_level(logging.ERROR)

    with open(CONFIG_FILE, "r+", encoding="UTF-8") as config_file_update:
        config_file_update_data = json.load(config_file_update)
        del config_file_update_data["title"]
        config_file_update.seek(0)
        config_file_update.write(json.dumps(config_file_update_data))
        config_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    log_present = False
    for record in caplog.records:
        print("Config validation failed!")
        if "Config validation failed!" in record.msg:
            print("Got here")
            log_present = True

    if log_present:
        assert True
    else:
        assert False


def test_config_no_description(caplog):
    caplog.set_level(logging.ERROR)

    with open(CONFIG_FILE, "r+", encoding="UTF-8") as config_file_update:
        config_file_update_data = json.load(config_file_update)
        del config_file_update_data["description"]
        config_file_update.seek(0)
        config_file_update.write(json.dumps(config_file_update_data))
        config_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    log_present = False
    for record in caplog.records:
        print("Config validation failed!")
        if "Config validation failed!" in record.msg:
            print("Got here")
            log_present = True

    if log_present:
        assert True
    else:
        assert False


def test_config_no_swagger_resource_type(caplog):
    caplog.set_level(logging.ERROR)

    with open(CONFIG_FILE, "r+", encoding="UTF-8") as config_file_update:
        config_file_update_data = json.load(config_file_update)
        del config_file_update_data["swagger_resource_type"]
        config_file_update.seek(0)
        config_file_update.write(json.dumps(config_file_update_data))
        config_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    log_present = False
    for record in caplog.records:
        print("Config validation failed!")
        if "Config validation failed!" in record.msg:
            print("Got here")
            log_present = True

    if log_present:
        assert True
    else:
        assert False


def test_config_no_swagger_default_network(caplog):
    caplog.set_level(logging.ERROR)

    with open(CONFIG_FILE, "r+", encoding="UTF-8") as config_file_update:
        config_file_update_data = json.load(config_file_update)
        del config_file_update_data["swagger_default_network"]
        config_file_update.seek(0)
        config_file_update.write(json.dumps(config_file_update_data))
        config_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    log_present = False
    for record in caplog.records:
        print("Config validation failed!")
        if "Config validation failed!" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


def test_resources_top_level_networks_missing(caplog):
    caplog.set_level(logging.ERROR)

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["networks"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    log_present = False
    for record in caplog.records:
        if "networks not found in resources" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


def test_resources_top_level_users_missing(caplog):
    caplog.set_level(logging.ERROR)

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["users"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    log_present = False
    for record in caplog.records:
        if "users not found in resources" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


def test_resources_top_level_databases_missing(caplog):
    caplog.set_level(logging.ERROR)

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["databases"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    log_present = False
    for record in caplog.records:
        if "databases not found in resources" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


def test_resources_top_level_systems_missing(caplog):
    caplog.set_level(logging.ERROR)

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["systems"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    log_present = False
    for record in caplog.records:
        if "systems not found in resources" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


def test_resources_networks_fields(caplog):
    caplog.set_level(logging.ERROR)

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resources_file_update:
        resources_file_update_data = json.load(resources_file_update)
        del resources_file_update_data["resources"]["networks"][0]["name"]
        resources_file_update.seek(0)
        resources_file_update.write(json.dumps(resources_file_update_data))
        resources_file_update.truncate()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.main()

    log_present = False
    for record in caplog.records:
        if "name not set for network" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "Required field not set for user" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "Required field not set for user" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "Required field not set for user" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "Required field not set for database" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "Required field not set for database" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "Required field not set for database" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "Required field not set for system" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "Required field not set for system" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "Required field not set for system" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "Required field not set for res_link" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "Required field not set for res_link" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "Required field not set for res_link" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "systems not found in defaults" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "systems not found in defaults" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "users not found in defaults" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "databases not found in defaults" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "networks not found in defaults" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "No paths provided in swagger.json" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False


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

    log_present = False
    for record in caplog.records:
        if "description not set on swagger path /api/user/add" in record.msg:
            log_present = True

    if log_present:
        assert True
    else:
        assert False
