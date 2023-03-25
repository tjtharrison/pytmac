"""
Python based programatic threat modelling tool tmacs
"""
import json
import logging
import os
import sys
from copy import deepcopy
from datetime import date

import yaml

try:
    print(len(os.environ.get("GITHUB_WORKSPACE")))
except TypeError:
    # Not GITHUB, load dotenv
    import dotenv  # pylint: disable=unused-import
    from dotenv import load_dotenv  # pylint: disable=unused-import

    load_dotenv()

from bin import input_validator, resource_validator

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


def main():
    """
    Main function used to open up provided config and resource files, generating DFD and output
    report
    :return: True
    """

    # Load resources
    with open(
        os.environ.get("RESOURCES_FILE"), "r", encoding="UTF-8"
    ) as resources_file:
        try:
            resources_yaml = yaml.safe_load(resources_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load RESOURCES_FILE: %s", error_message)

    # Load config

    with open(os.environ.get("CONFIG_FILE"), "r", encoding="UTF-8") as config_file:
        try:
            config_yaml = yaml.safe_load(config_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load CONFIG_FILE: %s", error_message)

    # Load defaults
    with open(os.environ.get("DEFAULTS_FILE"), "r", encoding="UTF-8") as defaults_file:
        try:
            defaults_yaml = yaml.safe_load(defaults_file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load DEFAULTS_FILE: %s", error_message)

    # Lets do some config validation
    if not input_validator.config(config_yaml):
        logging.error("Config validation failed!")
        sys.exit()
    if not input_validator.resources(resources_yaml):
        logging.error("Resources validation failed!")
        sys.exit()
    if not input_validator.defaults(defaults_yaml):
        logging.error("Defaults validation failed!")
        sys.exit()
    else:
        logging.info("All files validated successfully")

    resources = resources_yaml["resources"]

    # Load swagger if enabled
    if os.environ.get("ENABLE_SWAGGER").lower() == "true":
        # Load specified swagger file
        with open(
            os.environ.get("SWAGGER_FILE"), "r", encoding="UTF-8"
        ) as swagger_file:
            swagger_json = json.loads(swagger_file.read())

        if not input_validator.swagger(swagger_json):
            logging.error("Swagger validation failed!")
            sys.exit(1)

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
                == None
            ):
                resources_yaml["resources"][config_yaml["swagger_resource_type"]] = []
                resources_yaml["resources"][
                    config_yaml["swagger_resource_type"]
                ].append(swagger_path_detail)
            else:
                if (
                    type(
                        resources_yaml["resources"][
                            config_yaml["swagger_resource_type"]
                        ]
                    )
                    == dict
                ):
                    resources_yaml["resources"][
                        config_yaml["swagger_resource_type"]
                    ] | (swagger_path_detail)
                elif (
                    type(
                        resources_yaml["resources"][
                            config_yaml["swagger_resource_type"]
                        ]
                    )
                    == list
                ):
                    resources_yaml["resources"][
                        config_yaml["swagger_resource_type"]
                    ].append(swagger_path_detail)
    output_file_dir = os.environ.get("OUTPUT_DIR")
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
            for description_line in config_yaml["description"]:
                output_file.write(description_line + "\n\n")

            # Write wrapper for DFD
            output_file.write("# Data Flow Diagram\n")
            output_file.write("```plantuml\n")
            output_file.write("@startuml " + output_file_name + "\n")
            output_file.write(
                "!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml\n"
            )
            output_file.write(
                "!include https://raw.githubusercontent.com/geret1/plantuml-schemas/main/stride.puml\n"
            )
            output_file.write("\n")

            # Write networks wrapper
            output_yaml_report["networks"] = {}
            output_yaml_report["databases"] = {}
            output_yaml_report["users"] = {}
            output_yaml_report["systems"] = {}
            output_yaml_report["containers"] = {}
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

                # Look for containers in network
                try:
                    for container in resources["containers"]:
                        if container["network"] == network["name"]:
                            output_yaml_report["containers"][
                                container["name"]
                            ] = deepcopy(defaults_yaml["systems"])
                            # Look for override config for system
                            try:
                                logging.info("Overrides set for %s", container["name"])
                                for config_setting in container["config"]:
                                    logging.info(
                                        "Setting "
                                        + config_setting
                                        + " on "
                                        + container["name"]
                                    )
                                    output_yaml_report["containers"][container["name"]][
                                        config_setting
                                    ] = container["config"][config_setting]
                            except KeyError:
                                # No overrides set, nothing to do
                                logging.info("No overrides for %s", container["name"])

                            output_file.write(
                                "\t"
                                + "Container("
                                + container["name"].replace("/", "_")
                                + ","
                                + '"'
                                + container["name"]
                                + ' ", "'
                                + container["description"]
                                + '")'
                                + "\n"
                            )
                except TypeError:
                    logging.debug("No containers found")
                output_file.write("}" + "\n")
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
            output_file.write("![Diagram](./" + output_file_name + ".svg)")

            # Print final json
            yaml.dump(output_yaml_report, output_yaml)

            # Insecure resources
            insecure_resources = resource_validator.main(output_yaml_report)
            if len(insecure_resources) > 0:
                # Writing some auto threat modelling
                output_file.write(
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
    return True


if __name__ == "__main__":
    main()
