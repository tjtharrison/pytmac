import json
import logging
import os


def config(config_json):
    """
    Validate required fields in config.json

    :param config_json: Json structure containing the app running config
    :return: True/False
    """
    try:
        title = config_json["title"]
        description = config_json["description"]
        if os.environ.get("ENABLE_SWAGGER"):
            swagger_resource_type = config_json["swagger_resource_type"]
            swagger_default_network = config_json["swagger_default_network"]
    except KeyError:
        return False

    return True


def resources(resources_json):
    """
    Validate required fields in resources.json

    :param resources_json: Json structure containing the app resources
    :return: True/False
    """

    # Validate top level fields set
    resource_types = list(resources_json["resources"].keys())
    required_network_types = ["networks", "databases", "users", "systems"]
    for required_type in required_network_types:
        if required_type not in resource_types:
            logging.error(required_type + " not found in resources")
            return False

    # Validate network fields
    try:
        for network in resources_json["resources"]["networks"]:
            network_name = network["name"]
    except KeyError:
        logging.error("name not set for network: " + str(network))
        return False

    # Validate user fields
    try:
        for user in resources_json["resources"]["users"]:
            name = user["name"]
            network = user["network"]
            description = user["description"]
    except KeyError:
        logging.error(
            "Required field not set for user (Required: name, network, description): "
            + str(user)
        )
        return False

    # Validate database fields
    try:
        for database in resources_json["resources"]["databases"]:
            name = database["name"]
            network = database["network"]
            description = database["description"]
    except KeyError:
        logging.error(
            "Required field not set for database (Required: name, network, description): "
            + str(database)
        )
        return False

    # Validate systems fields
    try:
        for system in resources_json["resources"]["systems"]:
            name = system["name"]
            network = system["network"]
            description = system["description"]
    except KeyError:
        logging.error(
            "Required field not set for system (Required: name, network, description): "
            + str(system)
        )
        return False

    # Validate containers fields
    try:
        for container in resources_json["resources"]["containers"]:
            name = container["name"]
            network = container["network"]
            description = container["description"]
    except KeyError:
        logging.error(
            "Required field not set for container (Required: name, network, description): "
            + str(container)
        )
        return False

    # Validate res_link fields
    try:
        for res_link in resources_json["resources"]["res_links"]:
            source = res_link["source"]
            destination = res_link["destination"]
            description = res_link["description"]
    except KeyError:
        logging.error(
            "Required field not set for res_link (Required: source, destination, description): "
            + str(res_link)
        )
        return False

    return True


def defaults(defaults_json):
    """
    Validate required fields set in defaults.json

    :param defaults_json: Json structure containing resource defaults
    :return: True/False
    """
    resource_types = defaults_json.keys()

    required_network_types = ["networks", "databases", "users", "systems"]

    for required_type in required_network_types:
        if required_type not in resource_types:
            logging.error(required_type + " not found in defaults")
            return False
    return True


def swagger(swagger_json):
    """
    Validate required fields set in swagger.json (If ENABLE_SWAGGER is set to True)

    :param swagger_json: Json structure containing swagger file contents
    :return: True/False
    """
    if os.environ.get("ENABLE_SWAGGER"):
        # Validate paths exist
        if len(swagger_json["paths"]) < 1:
            logging.error("No paths provided in swagger.json")
            return False

        for swagger_path in swagger_json["paths"]:
            try:
                path_description = swagger_json["paths"][swagger_path][
                    str(list(swagger_json["paths"][swagger_path].keys())[0])
                ]["description"]
            except KeyError:
                logging.error("description not set on swagger path " + swagger_path)
                return False
    return True
