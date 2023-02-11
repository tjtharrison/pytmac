import json

from bin import checks

# Load config
with open("docs/config.json", "r", encoding="UTF-8") as config_file:
    config_json = json.loads(config_file.read())

with open("docs/security_checks.json", "r", encoding="UTF-8") as check_details_file:
    check_details = json.loads(check_details_file.read())

def main(output_json_report):
    """
    Function to collect responses from installed Security scans and Return to be written to the final report.

    Insecure resources are returned in the format:

    {
        "name": [The name of the check],
        "resource": [List of non-compliant resources],
        "description": [Description of what the check],
        "remediation": [Steps that should be taken to remediate the concern],
        "severity": [1-4 score on the impact of the insecurity]
    }

    :param output_json_report: A json document containing all resources and configuration settings included in the final
    report.
    :return: List of insecure resources.
    """
    insecure_resources = []

    for security_check in check_details:
        results = getattr(checks, security_check)()
        if len(results) > 0:
            for result in results:
                insecure_resources.append(result)

    print(insecure_resources)

    return insecure_resources

