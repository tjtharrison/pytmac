#!/usr/bin/env python3

"""Python based programmatic threat modelling tool tmacs."""
import argparse
import json
import logging
import os
import subprocess
import sys
from copy import deepcopy
from datetime import date

import inquirer
import yaml

from _version import __version__
from bin import get_config, init, input_validator, resource_validator

VERSION = __version__

# Configure logging
logging.basicConfig(
    format=(
        "{"
        '"time":"%(asctime)s",'
        ' "name": "%(name)s",'
        ' "level": "%(levelname)s",'
        ' "message": "%(message)s"'
        "}"
    ),
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Use argparse to add arguments
parser = argparse.ArgumentParser(
    prog="pytmac",
    description="Python based programmatic threat modelling tool",
)
parser.add_argument(
    "--version", action="store_true", help="Option to print the current version only"
)
parser.add_argument(
    "--demo",
    action="store_true",
    help="Run pytmac in demo mode using the demo config and resources",
)
parser.add_argument(
    "--output-dir",
    action="store",
    default=".",
    help="[Default: current ] Set the directory for report output",
)
parser.add_argument(
    "--resources-file",
    action="store",
    default="None",
    help="The path to the resources file",
)
parser.add_argument(
    "--config-file",
    action="store",
    default="None",
    help="The path to the config file",
)
parser.add_argument(
    "--defaults-file",
    action="store",
    default="None",
    help="The path to the defaults file",
)
parser.add_argument(
    "--security-checks-file",
    action="store",
    default="Default",
    help="[Default: security_checks.yaml] The path to the security-checks file",
)
parser.add_argument(
    "--swagger-file",
    action="store",
    default="None",
    help="[Default: None] The path to the swagger file (optional)",
)
parser.add_argument(
    "--init",
    action="store_true",
    help="Enable directory initialisation mode",
)

args = parser.parse_args()


def main(
    resources_yaml,
    config_yaml,
    defaults_yaml,
    security_checks_yaml,
    output_dir,
    swagger_json="",
):
    """Primary function used to open up provided config and resource files, generating DFD and output.

    Args:
        resources_yaml: The resources yaml file.
        config_yaml: The config yaml file.
        defaults_yaml: The defaults yaml file.
        security_checks_yaml: The security checks yaml file.
        output_dir: The output directory.
        swagger_json: The swagger json file (Default value = "").

    Returns:
        bool: The return value. True for success, False otherwise.

    """
    # Validate configuration
    if not input_validator.config(config_yaml):
        logging.error("Config validation failed!")
        sys.exit(1)

    # Validate resources
    if not input_validator.resources(resources_yaml):
        logging.error("Resources validation failed!")
        sys.exit(1)

    # Validate defaults
    if not input_validator.defaults(defaults_yaml):
        logging.error("Defaults validation failed!")
        sys.exit(1)

    # Validate swagger
    if swagger_json != "None":
        if not input_validator.swagger(swagger_json):
            logging.error("Swagger validation failed!")
            sys.exit(1)

    # Validate output directory exists
    if not os.path.exists(output_dir):
        logging.error("Output directory (%s) does not exist!", output_dir)
        sys.exit(1)

    resources = resources_yaml["resources"]
    # Load swagger if enabled
    if swagger_json != "None":
        swagger_json = json.loads(swagger_json)
        # Load swagger file
        swagger_paths = list(swagger_json["paths"].keys())
        for swagger_path in swagger_paths:
            swagger_path_detail = {
                "name": swagger_path,
                "network": config_yaml["swagger_default_network"],
                "description": swagger_json["paths"][swagger_path][
                    str(list(swagger_json["paths"][swagger_path].keys())[0])
                ]["description"],
            }
            # Append swagger endpoint to default swagger_resource_type resources
            if (
                resources_yaml["resources"][config_yaml["swagger_resource_type"]]
                is None
            ):
                resources_yaml["resources"][config_yaml["swagger_resource_type"]] = []
                resources_yaml["resources"][
                    config_yaml["swagger_resource_type"]
                ].append(swagger_path_detail)
            else:
                if isinstance(
                    resources_yaml["resources"][config_yaml["swagger_resource_type"]],
                    dict,
                ):
                    resources_yaml["resources"][
                        config_yaml["swagger_resource_type"]
                    ] | (swagger_path_detail)
                elif isinstance(
                    resources_yaml["resources"][config_yaml["swagger_resource_type"]],
                    list,
                ):
                    resources_yaml["resources"][
                        config_yaml["swagger_resource_type"]
                    ].append(swagger_path_detail)

    # Check if plantuml is callable
    try:
        # Check if plantuml executable is available
        subprocess.run(["plantuml", "-version"], stdout=subprocess.DEVNULL)
        logging.info("Plantuml executable found, will generate diagrams")
        plantuml_available = True
    except FileNotFoundError:
        plantuml_available = False
        logging.error("Plantuml executable not found, unable to generate diagram")

    output_file_dir = output_dir
    output_file_name = "report-" + str(date.today())

    with open(
        output_file_dir + "/" + output_file_name + ".md", "w+", encoding="UTF-8"
    ) as output_file:
        # Build out json report
        with open(
            output_file_dir + "/" + output_file_name + ".yaml", "w", encoding="UTF-8"
        ) as output_yaml:
            # Start empty json for output report
            output_yaml_report = {}
            # Write intro into markdown
            output_file.write("# " + config_yaml["title"] + "\n")
            if type(config_yaml["description"]) == list:
                for description_line in config_yaml["description"]:
                    output_file.write(description_line + "\n")
            else:
                output_file.write(config_yaml["description"])
            output_file.write("\n\n")

            # Write wrapper for DFD
            output_file.write("# Data Flow Diagram\n")
            output_file.write("```plantuml\n")
            output_file.write("@startuml " + output_file_name + "\n")
            output_file.write(
                "!include https://raw.githubusercontent.com/"
                "plantuml-stdlib/C4-PlantUML/master/C4_Container.puml\n"
            )
            output_file.write(
                "!include https://raw.githubusercontent.com/"
                "geret1/plantuml-schemas/main/stride.puml\n"
            )
            output_file.write("\n")

            # Write networks wrapper
            output_yaml_report["networks"] = {}
            output_yaml_report["databases"] = {}
            output_yaml_report["users"] = {}
            output_yaml_report["systems"] = {}
            # Process network resources as top wrapper
            for network in resources["networks"]:
                # Build out network config in output
                output_yaml_report["networks"][network["name"]] = deepcopy(
                    defaults_yaml["networks"]
                )

                # Look for override config for network
                try:
                    logging.info("Overrides set for %s", network["name"])
                    for config_setting in network["config"]:
                        logging.info(
                            "Setting " + config_setting + " on " + network["name"]
                        )
                        output_yaml_report["networks"][network["name"]][
                            config_setting
                        ] = network["config"][config_setting]
                except KeyError:
                    logging.info("No overrides set, nothing to do")
                # Write network to mermaid
                output_file.write(
                    "Boundary(b"
                    + network["name"]
                    + ', "'
                    + network["name"]
                    + '") {'
                    + "\n"
                )

                # Look for users in network
                for user in resources["users"]:
                    if user["network"] == network["name"]:
                        output_yaml_report["users"][user["name"]] = deepcopy(
                            defaults_yaml["users"]
                        )
                        # Look for override config
                        try:
                            logging.info("Overrides set for %s", user["name"])
                            for config_setting in user["config"]:
                                logging.info(
                                    "Setting " + config_setting + " on " + user["name"]
                                )
                                output_yaml_report["users"][user["name"]][
                                    config_setting
                                ] = user["config"][config_setting]
                        except KeyError:
                            # No overrides set, nothing to do
                            logging.info("No overrides for %s", user["name"])

                        output_file.write(
                            "\t"
                            + "Person("
                            + user["name"]
                            + ', "'
                            + user["name"]
                            + '", "'
                            + user["description"]
                            + '")'
                            + "\n"
                        )

                # Look for databases in network
                for database in resources["databases"]:
                    if database["network"] == network["name"]:
                        output_yaml_report["databases"][database["name"]] = deepcopy(
                            defaults_yaml["databases"]
                        )
                        # Look for override config for database
                        try:
                            logging.info("Overrides set for %s", database["name"])
                            for config_setting in database["config"]:
                                logging.info(
                                    "Setting "
                                    + config_setting
                                    + " on "
                                    + database["name"]
                                )
                                output_yaml_report["databases"][database["name"]][
                                    config_setting
                                ] = database["config"][config_setting]
                        except KeyError:
                            # No overrides set, nothing to do
                            logging.info("No overrides for %s", database["name"])

                        output_file.write(
                            "\t"
                            + "SystemDb("
                            + database["name"]
                            + ","
                            + '"'
                            + database["name"]
                            + ' ", "'
                            + database["description"]
                            + '")'
                            + "\n"
                        )

                # Look for systems in network
                for system in resources["systems"]:
                    if system["network"] == network["name"]:
                        output_yaml_report["systems"][system["name"]] = deepcopy(
                            defaults_yaml["systems"]
                        )
                        # Look for override config for system
                        try:
                            logging.info("Overrides set for %s", system["name"])
                            for config_setting in system["config"]:
                                logging.info(
                                    "Setting "
                                    + config_setting
                                    + " on "
                                    + system["name"]
                                )
                                output_yaml_report["systems"][system["name"]][
                                    config_setting
                                ] = system["config"][config_setting]
                        except KeyError:
                            # No overrides set, nothing to do
                            logging.info("No overrides for %s", system["name"])

                        output_file.write(
                            "\t"
                            + "System("
                            + system["name"].replace("/", "_")
                            + ","
                            + '"'
                            + system["name"]
                            + ' ", "'
                            + system["description"]
                            + '")'
                            + "\n"
                        )

            # Process links between resources
            for res_links in resources["res_links"]:
                output_file.write(
                    "BiRel("
                    + res_links["source"].replace("/", "_")
                    + ","
                    + res_links["destination"].replace("/", "_")
                    + ', "'
                    + res_links["description"]
                    + '")'
                    + "\n"
                )
            output_file.write("@enduml\n")
            output_file.write("```\n")
            output_file.write("\n")
            if plantuml_available:
                output_file.write("![Diagram](./" + output_file_name + ".svg)")

            # Print final json
            yaml.dump(output_yaml_report, output_yaml)

            # Insecure resources
            insecure_resources = resource_validator.main(
                security_checks_yaml, output_yaml_report
            )
            if len(insecure_resources) > 0:
                # Writing some auto threat modelling
                output_file.write(
                    "\n\n"
                    "| Name | Resources | Finding | Remediation | Query | Severity |"
                    "\n|-----|-----|-----|-----|-----|-----|\n"
                )
                for response in insecure_resources:
                    response_detail = (
                        "| "
                        + response["name"]
                        + " | "
                        + response["resource"]
                        + " | "
                        + response["description"]
                        + " | "
                        + response["remediation"]
                        + " | "
                        + response["check_query"]
                        + " | "
                        + str(response["severity"])
                        + " | "
                        + "\n"
                    )
                    output_file.write(response_detail)

    if plantuml_available:
        # Generate diagram
        subprocess.run(
            ["plantuml", "-tsvg", output_file_name + ".md"],
            stdout=subprocess.DEVNULL,
        )
        logging.info("DFD diagram generated")

    return True


if __name__ == "__main__":
    if args.version:
        print(VERSION)
        sys.exit(0)
    elif args.init:
        # Get config inputs from user
        try:
            project_config = init.get_inputs()
        except KeyboardInterrupt:
            print("\n\nOkay, maybe later!")
            sys.exit(1)

        # Create config file directory
        try:
            init.create_directory(project_config["config_directory"])
        except OSError:
            logging.error("Unable to create %s", project_config["config_directory"])
            sys.exit(1)

        # Create config file
        try:
            init.create_config_file(project_config)
        except OSError as error_message:
            print("Unable to get demo config file: " + str(error_message))
            sys.exit(1)
        except KeyError as error_message:
            print("Values provided are not valid" + str(error_message))
            sys.exit(1)
        except yaml.YAMLError as error_message:
            print("Unable to write config file: " + str(error_message))
            sys.exit(1)

        # Create defaults file
        try:
            init.create_defaults_file(project_config)
        except OSError:
            logging.error("Unable to write defaults file")
            sys.exit(1)
        except yaml.YAMLError:
            logging.error("Unable to write defaults file")
            sys.exit(1)

        # Set lists to blank
        users = []
        databases = []
        systems = []
        # Get networks
        try:
            networks = init.get_networks()
        except KeyboardInterrupt:
            print("\n\nOkay, maybe later!")
            sys.exit(1)

        for network in networks:
            network = network["name"]

            # Add some users
            try:
                users = init.get_users(network, users)
            except KeyboardInterrupt:
                print("\n\nOkay, maybe later!")
                sys.exit(1)

            # Add some databases
            try:
                databases = init.get_databases(network, databases)
            except KeyboardInterrupt:
                print("\n\nOkay, maybe later!")
                sys.exit(1)

            # Add some systems
            try:
                systems = init.get_systems(network, systems)
            except KeyboardInterrupt:
                print("\n\nOkay, maybe later!")
                sys.exit(1)

        all_resources = {
            "resources": {
                "networks": networks,
                "users": users,
                "databases": databases,
                "systems": systems,
            }
        }

        # Get all resources
        all_resource_names = init.get_resource_names(all_resources)

        # Create some links between resources
        try:
            links = init.get_links(all_resource_names)
        except KeyboardInterrupt:
            print("\n\nOkay, maybe later!")
            sys.exit(1)

        final_resources = {
            "resources": {
                "networks": networks,
                "users": users,
                "databases": databases,
                "systems": systems,
                "res_links": links,
            }
        }

        # Write resources to file
        try:
            init.create_resources_file(project_config, final_resources)
        except OSError:
            logging.error("Unable to write resources file")
            sys.exit(1)
        except yaml.YAMLError:
            logging.error("Unable to write resources file")
            sys.exit(1)

        # Create .pytmac file
        try:
            init.create_settings_file(project_config)
        except OSError:
            logging.error("Unable to write settings file")
            sys.exit(1)

        # Return summary
        init.return_summary(project_config)
        sys.exit(0)

    elif args.demo:
        logging.info("Running in demonstration mode")
        resources_input = get_config.resources("demo")
        config_input = get_config.config("demo")
        defaults_input = get_config.defaults("demo")
        security_checks_input = get_config.security_checks("default")
        SWAGGER_INPUT = get_config.swagger("demo")
    else:
        # Check if .pytmac file exists
        if os.path.isfile(".pytmac"):
            SETTINGS_FILE_EXISTS = True
            logging.info("Found .pytmac settings file")
            settings_input = get_config.settings()
        else:
            SETTINGS_FILE_EXISTS = False
            logging.info("No settings file found")

        error_response_list = []
        if str(args.resources_file) != "None" or (
            SETTINGS_FILE_EXISTS and "resource_file" in settings_input
        ):
            if str(args.resources_file) != "None":
                logging.info("Using resources file from command line")
                resource_source_file = args.resources_file
            else:
                resource_source_file = settings_input["resource_file"]
            resources_input = get_config.resources(resource_source_file)
        else:
            error_response_list.append(
                "resource-file is required, see --help for details"
            )

        if str(args.config_file) != "None" or (
            SETTINGS_FILE_EXISTS and "config_file" in settings_input
        ):
            if str(args.config_file) != "None":
                logging.info("Using config file from command line")
                config_source_file = args.config_file
            else:
                config_source_file = settings_input["config_file"]

            try:
                config_input = get_config.config(config_source_file)
            except Exception as error_message:
                error_response_list.append(
                    "Error loading config file: " + str(error_message)
                )
        else:
            error_response_list.append("config-file is required")

        if str(args.defaults_file) != "None" or (
            SETTINGS_FILE_EXISTS and "defaults_file" in settings_input
        ):
            if str(args.defaults_file) != "None":
                logging.info("Using defaults file from command line")
                defaults_source_file = args.defaults_file
            else:
                defaults_source_file = settings_input["defaults_file"]
            try:
                defaults_input = get_config.defaults(defaults_source_file)
            except Exception as error_message:
                error_response_list.append(
                    "Error loading defaults file: " + str(error_message)
                )
        else:
            error_response_list.append("defaults-file is required")

        if str(args.security_checks_file) != "Default" or (
            SETTINGS_FILE_EXISTS and "security_checks_file" in settings_input
        ):
            if str(args.security_checks_file) != "Default":
                logging.info("Using security checks file from command line")
                sec_source_file = args.security_checks_file
            else:
                sec_source_file = settings_input["security_checks_file"]
            security_checks_input = get_config.security_checks(sec_source_file)
        else:
            security_checks_input = get_config.security_checks("default")

        if str(args.swagger_file) != "None":
            logging.info("Using swagger file from command line")
            SWAGGER_INPUT = get_config.swagger(args.swagger_file)
        else:
            SWAGGER_INPUT = "None"

        if len(error_response_list) > 0:
            logging.error(
                "Error loading configuration files: "
                + ", ".join(error_response_list)
                + ". See --help for details"
            )
            sys.exit(1)

    main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        args.output_dir,
        SWAGGER_INPUT,
    )
