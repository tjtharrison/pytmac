"""
Modules to load the configuration files for pytmac from provided data files.
"""
import json
import logging
import os
import sys

import yaml

from bin import input_validator

docs_dir = os.path.join(os.path.dirname(__file__), "../", "docs")


def resources(file):
    """
    Function to return a list of resources to be included in the package
    :return: List of resources
    """
    if file == "demo":
        file = docs_dir + "/resources.yaml"
    with open(file, "r", encoding="UTF-8") as resources_file:
        try:
            resources_yaml = yaml.safe_load(resources_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load RESOURCE_FILE: %s", error_message)

    return resources_yaml


def config(file):
    """
    Function to return a list of config to be included in the package
    :return: List of resources
    """
    if file == "demo":
        file = docs_dir + "/config.yaml"

    with open(file, "r", encoding="UTF-8") as config_file:
        try:
            config_yaml = yaml.safe_load(config_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load CONFIG_FILE: %s", error_message)

    return config_yaml


def defaults(file):
    """
    Function to return a list of defaults to be included in the package
    :return: List of resources
    """
    if file == "demo":
        file = docs_dir + "/defaults.yaml"

    with open(file, "r", encoding="UTF-8") as default_file:
        try:
            default_yaml = yaml.safe_load(default_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load DEFAULTS_FILE: %s", error_message)

    return default_yaml


def security_checks(file):
    """
    Function to return a list of security_checks to be included in the package
    :return: List of resources
    """
    if file == "default":
        file = docs_dir + "/security_checks.yaml"

    with open(file, "r", encoding="UTF-8") as security_checks_file:
        try:
            security_checks_yaml = yaml.safe_load(security_checks_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load SECURITY_CHECKS_FILE: %s", error_message)

    return security_checks_yaml


def swagger(file):
    """
    Function to get and return swagger file contents
    :return: List of resources
    """

    if file == "demo":
        file = docs_dir + "/swagger.json"

    with open(file, "r", encoding="UTF-8") as swagger_file:
        try:
            swagger_json = json.loads(swagger_file.read())
        except Exception as error_message:
            logging.error("Failed to load SWAGGER_FILE: %s", error_message)

    return swagger_json
