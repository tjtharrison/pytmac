"""Modules to load the configuration files for pytmac from provided data files."""
import json
import os

import yaml

docs_dir = os.path.join(os.path.dirname(__file__), "../", "conf")


def resources(file):
    """Return a list of resources to be included in the package.

    Args:
        file: File to load resources from

    Returns:
        List of resources

    Raises:
        FileNotFoundError: If file is not found
        YAMLError: If file is not valid YAML

    """
    if file == "demo":
        file = docs_dir + "/resources.yaml"

    try:
        with open(file, "r", encoding="UTF-8") as resources_file:
            try:
                resources_yaml = yaml.safe_load(resources_file)
            except yaml.YAMLError as error_message:
                raise yaml.YAMLError("Failed to load RESOURCE_FILE: " + error_message)
    except FileNotFoundError as error_message:
        raise FileNotFoundError("No resources file found at " + file) from error_message

    return resources_yaml


def config(file):
    """Return a list of config to be included in the package.

    Args:
        file: File to load resources from

    Returns:
        List of resources

    Raises:
        FileNotFoundError: If file is not found
        YAMLError: If file is not valid YAML

    """
    if file == "demo":
        file = docs_dir + "/config.yaml"

    try:
        with open(file, "r", encoding="UTF-8") as config_file:
            try:
                config_yaml = yaml.safe_load(config_file)
            except yaml.YAMLError as error_message:
                raise yaml.YAMLError("Failed to load CONFIG_FILE: " + error_message)
    except FileNotFoundError as error_message:
        raise FileNotFoundError("No config file found at " + file) from error_message

    return config_yaml


def defaults(file):
    """Return a list of defaults to be included in the package.

    Args:
        file: File to load resources from

    Returns:
        List of resources

    Raises:
        FileNotFoundError: If file is not found
        YAMLError: If file is not valid YAML

    """
    if file == "demo":
        file = docs_dir + "/defaults.yaml"

    try:
        with open(file, "r", encoding="UTF-8") as default_file:
            try:
                default_yaml = yaml.safe_load(default_file)
            except yaml.YAMLError as error_message:
                raise yaml.YAMLError("Failed to load DEFAULTS_FILE: " + error_message)
    except FileNotFoundError as error_message:
        raise FileNotFoundError("No defaults file found at " + file) from error_message

    return default_yaml


def security_checks(file):
    """Return a list of security_checks to be included in the package.

    Args:
        file: File to load resources from

    Returns:
        List of resources

    Raises:
        FileNotFoundError: If file is not found
        YAMLError: If file is not valid YAML

    """
    if file == "default":
        file = docs_dir + "/security_checks.yaml"

    try:
        with open(file, "r", encoding="UTF-8") as security_checks_file:
            try:
                security_checks_yaml = yaml.safe_load(security_checks_file)
            except yaml.YAMLError as error_message:
                raise yaml.YAMLError(
                    "Failed to load SECURITY_CHECKS_FILE: " + error_message
                )

    except FileNotFoundError as error_message:
        raise FileNotFoundError(
            "No security_checks file found at " + file
        ) from error_message

    return security_checks_yaml


def swagger(file):
    """Get and return swagger file contents.

    Args:
        file: File to load resources from

    Returns:
        List of resources

    Raises:
        FileNotFoundError: If file is not found
        Exception: If file is not valid JSON

    """
    if file == "demo":
        file = docs_dir + "/swagger.json"

    try:
        with open(file, "r", encoding="UTF-8") as swagger_file:
            try:
                swagger_json = json.loads(swagger_file.read())
            except Exception as error_message:
                raise Exception(
                    "Failed to load SWAGGER_FILE: " + error_message
                ) from error_message
    except FileNotFoundError as error_message:
        raise FileNotFoundError(
            "No swagger.json file found at " + file
        ) from error_message

    return swagger_json


def settings():
    """Get and return settings file contents from .pytmac file.

    Returns:
        settings file contents

    Raises:
        FileNotFoundError: If file is not found
        YAMLError: If file is not valid YAML

    """
    try:
        with open(".pytmac", "r", encoding="UTF-8") as settings_file:
            try:
                settings_yaml = yaml.safe_load(settings_file)
            except yaml.YAMLError as error_message:
                raise yaml.YAMLError(
                    "Failed to load SECURITY_CHECKS_FILE: " + error_message
                )
    except FileNotFoundError as error_message:
        raise FileNotFoundError(
            "No .pytmac file found in current directory"
        ) from error_message

    return settings_yaml


def process_swagger(config_yaml, swagger_json):
    """Process swagger json file to return a list of endpoints.

    Args:
        config_yaml: config yaml file contents
        swagger_json: swagger json file contents

    Returns:
        List of endpoints

    """
    endpoints = []

    swagger_paths = list(swagger_json["paths"].keys())
    for swagger_path in swagger_paths:
        swagger_path_detail = {
            "name": swagger_path,
            "network": config_yaml["swagger_default_network"],
            "description": swagger_json["paths"][swagger_path][
                str(list(swagger_json["paths"][swagger_path].keys())[0])
            ]["description"],
        }
        endpoints.append(swagger_path_detail)

    return endpoints
