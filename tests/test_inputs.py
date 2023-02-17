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
            print("Got here")
            log_present = True

    if log_present:
        assert True
    else:
        assert False