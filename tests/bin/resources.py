import yaml
import os

RESOURCES_FILE = os.environ.get("RESOURCES_FILE")

def update(resource_block, contents):
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
