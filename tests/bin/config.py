import yaml
import os
import logging
import json

RESOURCES_FILE = os.environ.get("RESOURCES_FILE")
CONFIG_FILE = os.environ.get("CONFIG_FILE")
DEFAULTS_FILE = os.environ.get("DEFAULTS_FILE")
SECURITY_CHECKS_FILE = os.environ.get("SECURITY_CHECKS_FILE")
SWAGGER_FILE = os.environ.get("SWAGGER_FILE")

BACKUP_RESOURCES_FILE = RESOURCES_FILE.replace(".yaml", ".bak.yaml")
BACKUP_CONFIG_FILE = CONFIG_FILE.replace(".yaml", ".bak.yaml")
BACKUP_DEFAULTS_FILE = DEFAULTS_FILE.replace(".yaml", ".bak.yaml")
BACKUP_SWAGGER_FILE = SWAGGER_FILE.replace(".json", ".bak.json")

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

# Load swagger
with open(os.environ.get("SWAGGER_FILE"), encoding="UTF-8") as swagger_file_contents:
    swagger_json = json.loads(swagger_file_contents.read())


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

    with open(BACKUP_SWAGGER_FILE, "w+", encoding="UTF-8") as swagger_backup:
        swagger_backup.write(json.dumps(swagger_json))

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

    with open(BACKUP_SWAGGER_FILE, "r", encoding="UTF-8") as swagger_backup:
        backup_swagger_contents = json.loads(swagger_backup.read())
        with open(SWAGGER_FILE, "w+", encoding="UTF-8") as swagger_restore:
            swagger_restore.write(json.dumps(backup_swagger_contents))

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
    :param config_field: The field within config that requires deleting
    :return:
    """

    with open(CONFIG_FILE, "r", encoding="UTF-8") as config_file_update:
        try:
            config_yaml_all = yaml.safe_load(config_file_update)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load CONFIG_FILE: %s", error_message)

        del config_yaml_all[config_field]
        # Clobber the file
        try:
            with open(CONFIG_FILE, "w", encoding="UTF-8") as config_file_update:
                yaml.dump(config_yaml_all, config_file_update)

        except Exception as error_message:
            print(str(error_message))


def delete_resource(resource_field):
    """
    Delete value from resources file
    :param config_field: The field within resources that requires deleting
    :return:
    """

    with open(RESOURCES_FILE, "r+", encoding="UTF-8") as resource_file_update:
        try:
            resource_yaml_all = yaml.safe_load(resource_file_update)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load RESOURCES_FILE: %s", error_message)

        if "." not in resource_field:
            del resource_yaml_all["resources"][resource_field]
        else:
            del resource_yaml_all["resources"][resource_field.split(".")[0]][0][
                resource_field.split(".")[1]
            ]
        # Clobber the file
        try:
            with open(RESOURCES_FILE, "w", encoding="UTF-8") as resource_file_update:
                yaml.dump(resource_yaml_all, resource_file_update)
        except Exception as error_message:
            logging.error("Failed to rewrite file: %s", str(error_message))
            return False
    return True


def update_default_value(resource_type, resource_field, resource_value):

    with open(DEFAULTS_FILE, "r+", encoding="UTF-8") as default_file_update:
        try:
            defaults_yaml = yaml.safe_load(default_file_update)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load RESOURCES_FILE: %s", error_message)

        defaults_yaml[resource_type][resource_field] = resource_value
        default_file_update.seek(0)
        yaml.dump(defaults_yaml, default_file_update)
