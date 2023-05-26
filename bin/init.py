import os
from bin import get_config
import yaml
def get_inputs():
    try:
        print("Okay lets get your directory setup for pytmac!")
        project_name = input("First, what shall we name your project? ")
        project_description = input("What is your project about? ")
        config_directory = input(
            "Where shall we store your configuration files? (default: ./docs) "
        ) or "docs"
    except KeyboardInterrupt as error_message:

        raise KeyboardInterrupt from error_message

    return {
        "project_name": project_name,
        "project_description": project_description,
        "config_directory": config_directory,
    }

def create_directory(name):
    """
    Creates a directory if it does not exist

    :param name:
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
    Creates a config file for the project

    :param project_config:
    :return:
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
        with open(project_config["config_directory"] + "/config.yaml", "w", encoding="UTF-8") as config_file_update:
            yaml.dump(config_input, config_file_update)
    except yaml.YAMLError as error_message:
        raise yaml.YAMLError from error_message

    return True


def create_defaults_file(project_config):
    """
    Creates a defaults file for the project

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


def return_summary(project_config):
    """
    Returns a summary of the project configuration

    :param project_config:
    :return: True if summary was returned
    """

    print("\n",
        "Great! Project " + project_config["project_name"] + " created! 🫡",
        "You can now run pytmac with `pytmac` 🚀",
        "You can also run `pytmac --help` for more options 📚",
        "\n",
          "Happy threat modelling! 🕵️"
    )
