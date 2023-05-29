"""This file contains functions for creating a new pytmac project."""
import os

import inquirer
import yaml

from bin import get_config


def get_inputs():
    """
    Get user input for project configuration.

    :raises KeyboardInterrupt: if user cancels input

    :return: Dictionary with user input
    """
    try:
        print("Okay lets get your directory setup for pytmac!")
        project_name = input("First, what shall we name your project? ")
        project_description = input("What is your project about? ")
        config_directory = (
            input("Where shall we store your configuration files? (default: ./docs) ")
            or "docs"
        )
    except KeyboardInterrupt as error_message:
        raise KeyboardInterrupt from error_message

    return {
        "project_name": project_name,
        "project_description": project_description,
        "config_directory": config_directory,
    }


def create_directory(name):
    """
    Create a directory if it does not exist.

    :raises OSError: if directory cannot be created
    :param name: Name of directory to create
    :return: True if directory was created, False if it already exists
    """
    try:
        if not os.path.exists(name):
            os.makedirs(name)
        else:
            print("Directory already exists..")
    except OSError as error_message:
        print("Error: Creating directory. " + name)
        raise OSError from error_message

    return True


def create_config_file(project_config):
    """
    Create a config file for the project with user provided values.

    :raises OSError: if config file cannot be loaded
    :raises YAMLError: if values cannot be updated
    :raises KeyError: if config file cannot be created

    :param project_config: User provided input for project.
    :return: True if config file was created
    """
    # Get default config file
    try:
        config_input = get_config.config("demo")
    except OSError as error_message:
        print("Error: Getting default config file.")
        raise OSError from error_message

    # Update demo config with provided values
    try:
        config_input["title"] = project_config["project_name"]
        config_input["description"] = project_config["project_description"]
    except KeyError as error_message:
        raise KeyError from error_message

    try:
        with open(
            project_config["config_directory"] + "/config.yaml", "w", encoding="UTF-8"
        ) as config_file_update:
            yaml.dump(config_input, config_file_update)
    except yaml.YAMLError as error_message:
        raise yaml.YAMLError from error_message

    return True


def create_defaults_file(project_config):
    """
    Create a defaults file for the project.

    :raises OSError: if defaults file cannot be loaded
    :raises YAMLError: if values cannot be updated

    :param project_config: User provided input for project.
    :return: True if defaults file was created
    """
    defaults_file = project_config["config_directory"] + "/defaults.yaml"
    try:
        with open(defaults_file, "w", encoding="UTF-8") as defaults_file_update:
            yaml.dump(get_config.defaults("demo"), defaults_file_update)
    except OSError as error_message:
        raise OSError from error_message
    except yaml.YAMLError as error_message:
        raise yaml.YAMLError from error_message

    return True


def return_summary(project_config):
    """
    Return a summary of the project configuration.

    :param project_config: User provided input for project.
    :return: True if summary was returned
    """
    print(
        "\n".join(
            [
                "",
                "Great! Project " + project_config["project_name"] + " created! 🫡",
                "Config files stored in " + project_config["config_directory"] + " 📁",
                "You can now run pytmac with `pytmac` 🚀",
                "You can also run `pytmac --help` for more options 📚",
                "",
                "Happy threat modelling! 🕵️",
            ]
        )
    )

    return True


def create_resources_file(project_config, all_resources):
    """
    Create a resources file for the project.

    :raises OSError: if resources file cannot be loaded
    :raises YAMLError: if values cannot be updated


    :param project_config:  User provided input for project.
    :param all_resources: json file with all resources
    :return: True if resources file was created
    """
    resources_file = project_config["config_directory"] + "/resources.yaml"
    try:
        with open(resources_file, "w", encoding="UTF-8") as resources_file_update:
            yaml.dump(all_resources, resources_file_update)
    except OSError as error_message:
        raise OSError from error_message
    except yaml.YAMLError as error_message:
        raise yaml.YAMLError from error_message

    return True


def get_networks():
    """
    Get networks for project configuration.

    :return: List of networks
    """
    networks = []

    while True:
        if len(networks) > 0:
            more_networks = input(
                "Do you have any more networks to add? (yes/no) "
            ).lower()
            if more_networks == "yes":
                network_name = (
                    input("Please enter the name of your next network? ")
                    .replace(" ", "_")
                    .lower()
                )
                networks.append({"name": network_name})
            elif more_networks == "no":
                print("Moving on then..")
                break
            else:
                print("Please enter either yes or no. " + more_networks + " entered")
        else:
            network_name = (
                input("Please enter the name of your first network? ")
                .replace(" ", "_")
                .lower()
            )
            networks.append({"name": network_name})

    return networks


def get_users(network, users):
    """
    Get users for project configuration.

    :param network: Name of network
    :param users: List of users already added
    :return: List of users
    """
    while True:
        more_users = input(
            "Do you have any more users to add on network " + network + " ? (yes/no) "
        ).lower()
        if more_users == "yes":
            user_name = (
                input("Please enter the name of your user? ").replace(" ", "_").lower()
            )
            user_description = input(
                "Please enter a description for " + user_name + " ? "
            )
            users.append(
                {
                    "name": user_name,
                    "description": user_description,
                    "network": network,
                }
            )
        elif more_users == "no":
            break
        else:
            print("Please enter either yes or no. " + more_users + " entered")

        return users


def get_databases(network, databases):
    """
    Get databases for project configuration.

    :param network: Name of network
    :param databases: List of databases already added
    :return: list of databases
    """
    while True:
        more_databases = input(
            "Do you have any more databases to add on network "
            + network
            + " ? (yes/no) "
        ).lower()
        if more_databases == "yes":
            database_name = (
                input("Please enter the name of your database? ")
                .replace(" ", "_")
                .lower()
            )
            database_description = input(
                "Please enter a description for " + database_name + " ? "
            )
            databases.append(
                {
                    "name": database_name,
                    "description": database_description,
                    "network": network,
                }
            )
        elif more_databases == "no":
            break
        else:
            print("Please enter either yes or no. " + more_databases + " entered")

    return databases


def get_systems(network, systems):
    """
    Get systems for project configuration.

    :param network: Name of network
    :param systems: List of systems already added
    :return: list of systems
    """
    while True:
        more_systems = input(
            "Do you have any more systems to add on network " + network + " ? (yes/no) "
        ).lower()
        if more_systems == "yes":
            system_name = (
                input("Please enter the name of your system? ")
                .replace(" ", "_")
                .lower()
            )
            system_description = input(
                "Please enter a description for " + system_name + " ? "
            )
            systems.append(
                {
                    "name": system_name,
                    "description": system_description,
                    "network": network,
                }
            )
        elif more_systems == "no":
            break
        else:
            print("Please enter either yes or no. " + more_systems + " entered")

    return systems


def get_resource_names(all_resources):
    """
    Get all resource names from all_resources.

    :param all_resources: json file with all resources
    :return: List of resource names
    """
    all_resource_names = []
    for key in all_resources["resources"]:
        if key != "networks" and all_resources["resources"][key] is not None:
            for resource in all_resources["resources"][key]:
                all_resource_names.append(resource["name"])

    return all_resource_names


def get_links(all_resource_names):
    """
    Get links for project configuration.

    :param all_resource_names: List of all resource names
    :return: List of links
    """
    links = []
    # Create some links between resources
    while True:
        more_links = input("Do you have any more links to add? (yes/no) ").lower()
        if more_links == "yes":
            questions = [
                inquirer.List(
                    "source",
                    message="What is the source?",
                    choices=all_resource_names,
                ),
                inquirer.List(
                    "destination",
                    message="What is the destination?",
                    choices=all_resource_names,
                ),
            ]
            answers = inquirer.prompt(questions)

            link_desription = input(
                "Please enter a description for the link between "
                + answers["source"]
                + " and "
                + answers["destination"]
                + " ? "
            )

            links.append(
                {
                    "source": answers["source"],
                    "destination": answers["destination"],
                    "description": link_desription,
                }
            )
        elif more_links == "no":
            break
        else:
            print("Please enter either yes or no. " + more_links + " entered")

    return links


def create_settings_file(project_config):
    """
    Create settings file for project.

    :raises OSError: If unable to create settings file
    :param project_config: Project configuration
    :return: True if successful, False otherwise
    """
    try:
        with open(".pytmac", "w", encoding="utf-8") as settings_file:
            settings_file.write(
                'resource_file: "'
                + project_config["config_directory"]
                + '/resources.yaml"'
            )
        settings_file.write("\n")
        settings_file.write(
            'config_file: "' + project_config["config_directory"] + '/config.yaml"'
        )
        settings_file.write("\n")
        settings_file.write(
            'defaults_file: "' + project_config["config_directory"] + '/defaults.yaml"'
        )
        settings_file.write("\n")
    except OSError as error_message:
        raise OSError(error_message)

    return True
