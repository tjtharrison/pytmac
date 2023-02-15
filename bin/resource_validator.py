"""
Module used to initiate and collate security findings from the json report generated in the main
document function.
"""
import json
import logging


def main(output_json_report):
    """
    Function to collect responses from required security scans and return to be written to the final
    report.

    :param output_json_report: A json document containing all resources and configuration settings
    included in the final
    report.
    :return: List of insecure resources.
    """
    with open("docs/security_checks.json", "r", encoding="UTF-8") as check_details_file:
        check_details = json.loads(check_details_file.read())
    insecure_resources = []

    for security_check in check_details:
        logging.info("Starting security check " + security_check)
        results = do_check(output_json_report, check_details[security_check])
        if len(results) > 0:
            logging.info("Results found! Appending to insecure_resources")
            for result in results:
                insecure_resources.append(result)
        logging.info("Finished security check " + security_check)

    logging.info("Insecure resources: " + str(insecure_resources))
    return insecure_resources


def do_check(output_json_report, check_details):
    """
    Function that looks up a check type in security_checks.json and checks resources using a given
    function.

    Insecure resources are returned in the format:

    [{
        "name": [The name of the check],
        "resource": [List of non-compliant resources],
        "description": [Description of what the check],
        "remediation": [Steps that should be taken to remediate the concern],
        "severity": [1-4 score on the impact of the insecurity]
    }]

    :param output_json_report: The json report of resources and configuration
    :param check_details: A json containing the details for the check to run.
    :return: list(dict)
    """
    resources = {}
    for resource_scope in check_details["resource_scope"]:
        resources = resources | output_json_report[resource_scope]

    insecure_resources = []

    for resource in resources:
        if eval("".join(check_details["check_query"])):  # pylint: disable=eval-used
            example_resource = {
                "name": check_details["name"],
                "resource": resource,
                "description": check_details["description"],
                "remediation": check_details["remediation"],
                "severity": check_details["severity"],
            }

            insecure_resources.append(example_resource)

    return insecure_resources
