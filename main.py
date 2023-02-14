"""
Python based programatic threat modelling tool tmacs
"""
import json
import logging
import os
from copy import deepcopy
from datetime import date


try:
    print(len(os.environ.get("GITHUB_WORKSPACE")))
except TypeError:
    # Not GITHUB, load dotenv
    import dotenv
    from dotenv import load_dotenv
    load_dotenv()

from bin import resource_validator

# Configure logging
# Setup json logging
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
        resources_json = json.loads(resources_file.read())

    # Load config
    with open(os.environ.get("CONFIG_FILE"), "r", encoding="UTF-8") as config_file:
        config_json = json.loads(config_file.read())

    # Load defaults
    with open(os.environ.get("DEFAULTS_FILE"), "r", encoding="UTF-8") as defaults_file:
        defaults_json = json.loads(defaults_file.read())

    resources = resources_json["resources"]

    output_file_dir = os.environ.get("OUTPUT_DIR")
    output_file_name = "report-" + str(date.today())

    with open(
        output_file_dir + "/" + output_file_name + ".md", "w", encoding="UTF-8"
    ) as output_file:
        # Build out json report
        with open(
            output_file_dir + "/" + output_file_name + ".json", "w", encoding="UTF-8"
        ) as output_json:
            # Start empty json for output report
            output_json_report = {}
            # Write intro into markdown
            output_file.write("# " + config_json["title"] + "\n")
            for description_line in config_json["description"]:
                output_file.write(description_line + "\n\n")

            # Write wrapper for DFD
            output_file.write("# Data Flow Diagram\n")
            output_file.write("```mermaid")
            output_file.write("\n")
            output_file.write("C4Context")
            output_file.write("\n")

            # Write networks wrapper
            output_json_report["networks"] = {}
            output_json_report["databases"] = {}
            output_json_report["users"] = {}
            output_json_report["systems"] = {}
            output_json_report["containers"] = {}
            # Process network resources as top wrapper
            for network in resources["networks"]:
                # Build out network config in output
                output_json_report["networks"][network["name"]] = deepcopy(
                    defaults_json["networks"]
                )

                # Look for override config for network
                try:
                    logging.info("Overrides set for %s", network["name"])
                    for config_setting in network["config"]:
                        logging.info(
                            "Setting " + config_setting + " on " + network["name"]
                        )
                        output_json_report["networks"][network["name"]][
                            config_setting
                        ] = network["config"][config_setting]
                except KeyError:
                    logging.info("No overrides set, nothing to do")
                # Write network to mermaid
                output_file.write(
                    "\t"
                    + "Boundary(b"
                    + network["name"]
                    + ', "'
                    + network["name"]
                    + '") {'
                    + "\n"
                )

                # Look for users in network
                for user in resources["users"]:
                    if user["network"] == network["name"]:
                        output_json_report["users"][user["name"]] = deepcopy(
                            defaults_json["users"]
                        )
                        # Look for override config
                        try:
                            logging.info("Overrides set for %s", user["name"])
                            for config_setting in user["config"]:
                                logging.info(
                                    "Setting " + config_setting + " on " + user["name"]
                                )
                                output_json_report["users"][user["name"]][
                                    config_setting
                                ] = user["config"][config_setting]
                        except KeyError:
                            # No overrides set, nothing to do
                            logging.info("No overrides for %s", user["name"])

                        output_file.write(
                            "\t\t"
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
                        output_json_report["databases"][database["name"]] = deepcopy(
                            defaults_json["databases"]
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
                                output_json_report["databases"][database["name"]][
                                    config_setting
                                ] = database["config"][config_setting]
                        except KeyError:
                            # No overrides set, nothing to do
                            logging.info("No overrides for %s", database["name"])

                        output_file.write(
                            "\t\t"
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
                        output_json_report["systems"][system["name"]] = deepcopy(
                            defaults_json["systems"]
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
                                output_json_report["systems"][system["name"]][
                                    config_setting
                                ] = system["config"][config_setting]
                        except KeyError:
                            # No overrides set, nothing to do
                            logging.info("No overrides for %s", system["name"])

                        output_file.write(
                            "\t\t"
                            + "System("
                            + system["name"]
                            + ","
                            + '"'
                            + system["name"]
                            + ' ", "'
                            + system["description"]
                            + '")'
                            + "\n"
                        )

                # Look for containers in network
                for container in resources["containers"]:
                    if container["network"] == network["name"]:
                        output_json_report["containers"][container["name"]] = deepcopy(
                            defaults_json["containers"]
                        )
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
                                output_json_report["containers"][container["name"]][
                                    config_setting
                                ] = container["config"][config_setting]
                        except KeyError:
                            # No overrides set, nothing to do
                            logging.info("No overrides for %s", container["name"])

                        output_file.write(
                            "\t\t"
                            + "Container("
                            + container["name"]
                            + ","
                            + '"'
                            + container["name"]
                            + ' ", "'
                            + container["description"]
                            + '")'
                            + "\n"
                        )
                output_file.write("\t" + "}" + "\n")

            # Process links between resources
            for res_links in resources["res_links"]:
                output_file.write(
                    "\t"
                    + "BiRel("
                    + res_links["source"]
                    + ","
                    + res_links["destination"]
                    + ', "'
                    + res_links["description"]
                    + '")'
                    + "\n"
                )
                output_file.write("\n")
            output_file.write(
                'UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="3")' + "\n"
            )
            output_file.write("```\n")

            # Print final json
            final_report = json.dumps(output_json_report)

            output_json.write(final_report)

            # Insecure resources
            insecure_resources = resource_validator.main(output_json_report)
            if len(insecure_resources) > 0:
                # Writing some auto threat modelling
                output_file.write(
                    "| Name | Resources | Finding | Remediation | Severity |"
                    "\n|-----|-----|-----|-----|-----|\n"
                )
                for response in resource_validator.main(output_json_report):
                    check_name = response["name"]
                    check_description = response["description"]
                    check_resource = response["resource"]
                    check_remediation = response["remediation"]
                    check_severity = response["severity"]

                    output_file.write(
                        "| "
                        + check_name
                        + " | "
                        + check_resource
                        + " | "
                        + check_description
                        + " | "
                        + check_remediation
                        + " | "
                        + str(check_severity)
                        + " | "
                    )
    return True


if __name__ == "__main__":
    main()
