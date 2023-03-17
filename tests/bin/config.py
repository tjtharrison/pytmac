import yaml
import os
import logging

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


def backup():
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


def restore():
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

def delete_config(config_field):
    """
    Delete value from config file
    :param resource_block: The block within resources that requires updating
    :param contents: The dictionary to append onto the existing resources
    :return:
    """

    with open(CONFIG_FILE, "r+", encoding="UTF-8") as config_file_update:
        try:
            config_yaml_all = yaml.safe_load(config_file_update)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load CONFIG_FILE: %s", error_message)

        del config_yaml_all[config_field]
        print(config_yaml_all)
        config_file_update.seek(0)
        try:
            yaml.dump(config_yaml_all, config_file_update, default_flow_style=False)
        except Exception as error_message:
            print(str(error_message))
