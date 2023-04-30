import yaml
import logging
import json
import sys
from bin import input_validator as input_validator

def get_contents(file_name):
    """
    Get the contents of a specified file
    :param file_name: The name of the file to load
    :return:
    """
    with open(
            "docs/" + file_name + ".yaml", "r", encoding="UTF-8"
    ) as file:
        try:
            file_contents = yaml.safe_load(file)
        except yaml.YAMLError as error_message:
            logging.error("Failed to load SECURITY_CHECKS_FILE: %s", error_message)

    return file_contents


# Load files for demonstration
demo_config = {'title': 'tmac', 'description': ['This is an example of how tmac can be used to threat model your workload', 'It can handle multiple paragraphs in the description'], 'swagger_resource_type': 'containers', 'swagger_default_network': 'office_network'}
demo_defaults = {'databases': {'audit_logging_alerts': True, 'audit_logging_enabled': True, 'audit_logging_monitored': True, 'audit_logging_tamper_proof': True, 'audit_logging_to_siem': True, 'authentication_required': True, 'automatic_updates': True, 'cleanup_tasks_configured': True, 'contains_pii': True, 'database_os': 'MySQL', 'default_accounts_enabled': True, 'firewall_restricted': True, 'has_scheduled_backup': True, 'incident_response_runbooks': True, 'is_encrypted': True, 'is_hardened': True, 'is_replica': True, 'least_privileged_access': True, 'least_privileged_network': True, 'least_privileged_users': True, 'passwords_hashed': True, 'requires_encrypted_connections': True, 'secure_logging_enabled': True, 'tested_recovery_process': True}, 'networks': {'has_wifi': False, 'is_cloud': False, 'is_public': False}, 'systems': {'access_logging_enabled': True, 'allows_manual_changes': True, 'audit_logging_alerts': True, 'audit_logging_enabled': True, 'audit_logging_includes_user_details': True, 'audit_logging_monitored': True, 'audit_logging_tamper_proof': True, 'audit_logging_to_siem': True, 'authentication_required': True, 'automatic_updates': True, 'code_review_required': True, 'code_scan_in_pipeline': True, 'cors_minimal_required_usage': True, 'db_op': True, 'default_accounts_enabled': True, 'delayed_login_failures': True, 'dependabot_used': True, 'dependency_signing_required': True, 'has_secure_password_policy': True, 'has_waf': True, 'incident_response_runbooks': True, 'input_sanitization': True, 'input_validation': True, 'ip_restrictions': True, 'is_hardened': True, 'least_privileged_access': True, 'least_privileged_network': True, 'login_failures_logged': True, 'mfa_enabled': True, 'password_username_incorrect_same_message': True, 'public_facing': True, 'requires_authentication': True, 'requires_encryption': True, 'secret_scanning_used': True, 'secure_logging_enabled': True, 'security_scan_on_artifact_storage': True, 'security_scan_on_build': True, 'sessions_stored_securely': True, 'stateful_sessions_invalidated': True, 'tested_recovery_process': True}, 'users': {'company_device': True, 'company_user': True, 'uses_mfa': True, 'uses_own_login': True}}
demo_resources = {'resources': {'networks': [{'name': 'office_network'}, {'name': 'home_network'}], 'users': [{'name': 'user1', 'network': 'home_network', 'description': 'Database Administrator'}], 'databases': [{'name': 'staging', 'network': 'office_network', 'description': 'Staging database'}], 'systems': [{'name': 'vpn_server', 'network': 'office_network', 'description': 'VPN Server', 'config': {'db_op': False}}], 'containers': None, 'res_links': [{'source': 'user1', 'destination': 'vpn_server', 'description': 'User connects to VPN into office_network'}, {'source': 'vpn_server', 'destination': '/api/user/add', 'description': '/api/user/add accessed from the VPN server'}, {'source': 'vpn_server', 'destination': '/api/user', 'description': '/api/user accessed from the VPN server'}, {'source': '/api/user/add', 'destination': 'staging', 'description': '/api/user/add and adds data in the staging database'}, {'source': '/api/user', 'destination': 'staging', 'description': '/api/user gets data from the staging database'}]}}
demo_swagger_json = json.dumps({"tags": [], "paths": {"/api/user/add": {"post": {"description": "Receive requests from client to write users to database.", "operationId": "api_user_add", "parameters": [{"in": "body", "required": False, "name": "User", "schema": {"$ref": "#/components/schemas/User"}}], "responses": {"200": {"description": "OK, list of users under details", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Response"}}}}, "500": {"description": "Server error", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Response"}}}}}}}, "/api/user": {"get": {"description": "Endpoint to list all users from Database", "operationId": "api_user", "responses": {"200": {"description": "OK", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Response"}}}}, "500": {"description": "Server error", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Response"}}}}}}}}, "info": {"title": "Threat Modelling Demo", "version": "1.0.0"}, "openapi": "3.0.2", "components": {"schemas": {"Response": {"type": "object", "properties": {"details": {"type": "string"}, "status": {"type": "string"}}, "required": ["details", "status"]}, "User": {"type": "object", "properties": {"user_name": {"type": "string"}}, "required": ["user_name"]}}}})

# Load the default config
default_security_checks = {'user_owned_device': {'name': 'Non company device used', 'description': 'Checks for users with company_user true and company_device false.', 'remediation': 'Understand and remediate or document known exception.', 'severity': 1, 'resource_scope': ['users'], 'check_query': ['resources[resource]["company_user"] and not resources[resource]["company_device"]']}, 'broken_access_control': {'name': 'A01:2021-Broken Access Control', 'description': 'OWASP top 10 #1: Checks for combination of controls that indicate lack of mitigation against this type of attack', 'remediation': 'Review non-compliant controls and remediate', 'severity': 1, 'resource_scope': ['systems', 'containers'], 'check_query': ['not resources[resource]["requires_authentication"] ', 'or not resources[resource]["least_privileged_access"] ', 'or not resources[resource]["access_logging_enabled"] ', 'or not resources[resource]["cors_minimal_required_usage"] ', 'or not resources[resource]["stateful_sessions_invalidated"] ']}, 'cryptographic_failures': {'name': 'A02:2021-Cryptographic_Failures', 'description': 'OWASP top 10 #2: Checks for various items related to encryption', 'remediation': 'Review non-compliant controls and remediate', 'severity': 1, 'resource_scope': ['databases'], 'check_query': ['not resources[resource]["is_encrypted"] ', 'or not resources[resource]["cleanup_tasks_configured"] ', 'or not resources[resource]["requires_encrypted_connections"] ', 'or not resources[resource]["authentication_required"] ', 'or not resources[resource]["passwords_hashed"] ']}, 'sql_injection': {'name': 'A03:2021 – Injection', 'description': 'OWASP top 10 #3: Checks for mitigations against SQL injection', 'remediation': 'Review non-compliant controls and remediate', 'severity': 1, 'resource_scope': ['systems', 'containers'], 'check_query': ['(', ' not resources[resource]["input_sanitization"] ', ' or not resources[resource]["authentication_required"]', ' or not resources[resource]["is_hardened"]', ') and resources[resource]["db_op"]']}, 'insecure_design': {'name': 'A04:2021 – Insecure Design', 'description': 'OWASP top 10 #4: Checks for good Software development practices', 'remediation': 'Review non-compliant controls and remediate', 'severity': 1, 'resource_scope': ['systems', 'containers'], 'check_query': [' not resources[resource]["dependabot_used"] ', ' or not resources[resource]["secret_scanning_used"]', ' or not resources[resource]["least_privileged_access"]', ' or not resources[resource]["least_privileged_network"]']}, 'security_misconfig': {'name': 'A05:2021 – Security Misconfiguration', 'description': 'OWASP top 10 #5: Review for security misconfigurations', 'remediation': 'Review non-compliant controls and remediate', 'severity': 1, 'resource_scope': ['systems', 'containers', 'databases'], 'check_query': [' not resources[resource]["is_hardened"] ', ' or not resources[resource]["least_privileged_access"]', ' or not resources[resource]["least_privileged_network"]', ' or not resources[resource]["default_accounts_enabled"]', ' or not resources[resource]["secure_logging_enabled"]', ' or not resources[resource]["automatic_updates"]']}, 'vulnerable_components': {'name': 'A06:2021 – Vulnerable and Outdated Components', 'description': 'OWASP top 10 #6: Review for outdated or insecure dependencies', 'remediation': 'Review non-compliant controls and remediate', 'severity': 1, 'resource_scope': ['systems', 'containers'], 'check_query': [' not resources[resource]["dependabot_used"] ', ' or not resources[resource]["automatic_updates"]', ' or not resources[resource]["security_scan_on_build"]', ' or not resources[resource]["security_scan_on_artifact_storage"]']}, 'auth_failures': {'name': 'A07:2021 – Identification and Authentication Failures', 'description': 'OWASP top 10 #7: Identification and Authentication Failures', 'remediation': 'Review non-compliant controls and remediate', 'severity': 1, 'resource_scope': ['systems', 'containers'], 'check_query': [' not resources[resource]["mfa_enabled"] ', ' or not resources[resource]["default_accounts_enabled"]', ' or not resources[resource]["has_secure_password_policy"]', ' or not resources[resource]["password_username_incorrect_same_message"]', ' or not resources[resource]["delayed_login_failures"]', ' or not resources[resource]["login_failures_logged"]', ' or not resources[resource]["sessions_stored_securely"]']}, 'integrity_failure': {'name': 'A08:2021 – Software and Data Integrity Failures', 'description': 'OWASP top 10 #8: Software and Data Integrity Failures', 'remediation': 'Review non-compliant controls and remediate', 'severity': 1, 'resource_scope': ['systems', 'containers'], 'check_query': [' not resources[resource]["dependabot_used"] ', ' or not resources[resource]["dependency_signing_required"]', ' or not resources[resource]["code_review_required"]', ' or not resources[resource]["code_scan_in_pipeline"]', ' or not resources[resource]["code_scan_in_pipeline"]']}, 'logging_monitoring_failure': {'name': 'A09:2021 – Security Logging and Monitoring Failures', 'description': 'OWASP top 10 #9: Security Logging and Monitoring Failures', 'remediation': 'Review non-compliant controls and remediate', 'severity': 1, 'resource_scope': ['systems', 'containers', 'databases'], 'check_query': [' not resources[resource]["audit_logging_enabled"] ', ' or not resources[resource]["audit_logging_to_siem"]', ' or not resources[resource]["audit_logging_tamper_proof"]', ' or not resources[resource]["audit_logging_monitored"]', ' or not resources[resource]["audit_logging_alerts"]', ' or not resources[resource]["incident_response_runbooks"]', ' or not resources[resource]["tested_recovery_process"]']}, 'ssrf': {'name': 'A10:2021 – Server-Side Request Forgery (SSRF)', 'description': 'OWASP top 10 #10: Server-Side Request Forgery (SSRF)', 'remediation': 'Review non-compliant controls and remediate', 'severity': 1, 'resource_scope': ['systems', 'containers'], 'check_query': [' not resources[resource]["least_privileged_network"] ', ' or not resources[resource]["input_validation"]', ' or not resources[resource]["input_sanitization"]', ' or not resources[resource]["least_privileged_access"]', ' or not resources[resource]["requires_encryption"]']}, 'spoofing_users': {'name': 'STRIDE - Spoofing', 'description': 'A spoofing attack is a situation in which a person or program successfully identifies as another by falsifying data, to gain an illegitimate advantage', 'remediation': 'Ensure multiple methods of authentication are required for a user to verify their identity', 'severity': 1, 'resource_scope': ['users'], 'check_query': [' not resources[resource]["uses_mfa"] ']}, 'repudiation_user': {'name': 'STRIDE - Repudiation', 'description': 'Repudiation is the ability to associate actions taken on a system with a specific user', 'remediation': 'Ensure users do not use shared accounts', 'severity': 1, 'resource_scope': ['users'], 'check_query': [' not resources[resource]["uses_own_login"] ']}, 'repudiation_system': {'name': 'STRIDE - Repudiation', 'description': 'Repudiation is the ability to associate actions taken on a system with a specific user', 'remediation': 'Ensure logging contains identifiable information about the actor (Eg username, ip address)', 'severity': 1, 'resource_scope': ['systems'], 'check_query': [' not resources[resource]["audit_logging_includes_user_details"] ']}}

#### https://setuptools.pypa.io/en/latest/userguide/datafiles.html

def resources(file):
    """
    Function to return a list of resources to be included in the package
    :return: List of resources
    """
    if file == "demo":
        resources_yaml = demo_resources
    else:
        with open(file, "r", encoding="UTF-8") as resources_file:
            try:
                resources_yaml = yaml.safe_load(resources_file)
            except yaml.YAMLError as error_message:
                logging.error("Failed to load RESOURCE_FILE: %s", error_message)

    if not input_validator.resources(resources_yaml):
        logging.error("Resources validation failed!")
        sys.exit()

    return resources_yaml

def config(file):
    """
    Function to return a list of config to be included in the package
    :return: List of resources
    """
    if file == "demo":
        config_yaml = demo_config
    else:
        with open(file, "r", encoding="UTF-8") as config_file:
            try:
                config_yaml = yaml.safe_load(config_file)
            except yaml.YAMLError as error_message:
                logging.error("Failed to load CONFIG_FILE: %s", error_message)
    if not input_validator.config(config_yaml):
        logging.error("Config validation failed!")
        sys.exit()

    return config_yaml

def defaults(file):
    """
    Function to return a list of defaults to be included in the package
    :return: List of resources
    """
    if file == "demo":
        default_yaml = demo_defaults
    else:
        with open(file, "r", encoding="UTF-8") as default_file:
            try:
                default_yaml = yaml.safe_load(default_file)
            except yaml.YAMLError as error_message:
                logging.error("Failed to load DEFAULTS_FILE: %s", error_message)

    if not input_validator.defaults(default_yaml):
        logging.error("Defaults validation failed!")
        sys.exit()

    return default_yaml

def defaults(file):
    """
    Function to return a list of defaults to be included in the package
    :return: List of resources
    """
    if file == "demo":
        default_yaml = demo_defaults
    else:
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
        security_checks_yaml = default_security_checks
    else:
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
        swagger_json = demo_swagger_json
    else:
        with open(file, "r", encoding="UTF-8") as swagger_file:
            try:
                swagger_json = json.loads(swagger_file.read())
            except Exception as error_message:
                logging.error("Failed to load SWAGGER_FILE: %s", error_message)

    if not input_validator.swagger(swagger_json):
        logging.error("Swagger validation failed!")
        sys.exit(1)

    return swagger_json
