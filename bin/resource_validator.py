import json

# Load config
with open("docs/config.json", "r", encoding="UTF-8") as config_file:
    config_json = json.loads(config_file.read())

with open("docs/security_checks.json", "r", encoding="UTF-8") as check_details_file:
    check_details = json.loads(check_details_file.read())

with open("docs/security_checks.json", "r", encoding="UTF-8") as check_details_file:
    check_details = json.loads(check_details_file.read())


def main(output_json_report):
    """
    Function to collect responses from required security scans and return to be written to the final report.

    :param output_json_report: A json document containing all resources and configuration settings included in the final
    report.
    :return: List of insecure resources.
    """
    insecure_resources = []

    for security_check in check_details:
        results = do_check(security_check, output_json_report)
        if len(results) > 0:
            for result in results:
                insecure_resources.append(result)

    return insecure_resources


def do_check(check_type, output_json_report):
    """
    Function that looks up a check type in security_checks.json and checks resources using a given function.

    Insecure resources are returned in the format:

    [{
        "name": [The name of the check],
        "resource": [List of non-compliant resources],
        "description": [Description of what the check],
        "remediation": [Steps that should be taken to remediate the concern],
        "severity": [1-4 score on the impact of the insecurity]
    }]

    :param check_type: The name of the check to look up
    :param output_json_report: The json report of resources and configuration
    :return: list(dict)
    """

    this_check = check_details[check_type]
    resources = output_json_report[this_check["resource_scope"]]
    insecure_resources = []

    for resource in resources:
        if eval(this_check["check_query"]):
            example_resource = {
                "name": this_check["name"],
                "resource": resource,
                "description": this_check["description"],
                "remediation": this_check["remediation"],
                "severity": this_check["severity"],
            }

            insecure_resources.append(example_resource)

    return insecure_resources
