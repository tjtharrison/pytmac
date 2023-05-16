[![FOSSA Status](https://app.fossa.com/api/projects/custom%2B37707%2Fgit%40github.com%3Atjtharrison%2Ftmac.git.svg?type=shield)](https://app.fossa.com/projects/custom%2B37707%2Fgit%40github.com%3Atjtharrison%2Ftmac.git?ref=badge_shield)
![Workflow Actionlint](https://github.com/tjtharrison/pytmac/actions/workflows/pr-actionlint.yaml/badge.svg)
![Workflow Checkov](https://github.com/tjtharrison/pytmac/actions/workflows/pr-checkov.yaml/badge.svg)
![Workflow Linting](https://github.com/tjtharrison/pytmac/actions/workflows/pr-linting.yaml/badge.svg)
![Workflow Unit Tests](https://github.com/tjtharrison/pytmac/actions/workflows/pr-tests.yaml/badge.svg)
![Workflow CodeQL](https://github.com/tjtharrison/pytmac/actions/workflows/pr-codeql.yaml/badge.svg)

# pytmac

Python based threat modelling as code tool (Python T.M.A.C).

pytmac generates a report of a designated workload given a combination of manually created resources, configured checks 
and custom checks.

## Resources

Manual resources can be added to `./docs/resources.yaml` and should be in the following format.

```
---
resources:
  networks:
    - name: office_network
    - name: home_network
  users:
    - name: user1
      network: home_network
      description: Database Administrator
  databases:
    - name: staging
      network: office_network
      description: Staging database
  systems:
    - name: vpn_server
      network: office_network
      description: VPN Server
      config:
        db_op: false
  containers:
  res_links:
    - source: user1
      destination: vpn_server
      description: User connects to VPN into office_network
    - source: vpn_server
      destination: "/api/user/add"
      description: "/api/user/add accessed from the VPN server"
    - source: vpn_server
      destination: "/api/user"
      description: "/api/user accessed from the VPN server"
    - source: "/api/user/add"
      destination: staging
      description: "/api/user/add and adds data in the staging database"
    - source: "/api/user"
      destination: staging
      description: "/api/user gets data from the staging database"
```

The above yaml content will be processed and generate the following DFD (Data Flow Diagram) in PlantUML.

```
@startuml report-2023-03-25
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml
!include https://raw.githubusercontent.com/geret1/plantuml-schemas/main/stride.puml

Boundary(boffice_network, "office_network") {
	SystemDb(staging,"staging ", "Staging database")
	System(vpn_server,"vpn_server ", "VPN Server")
	Container(_api_user_add,"/api/user/add ", "Receive requests from client to write users to database.")
	Container(_api_user,"/api/user ", "Endpoint to list all users from Database")
}
Boundary(bhome_network, "home_network") {
	Person(user1, "user1", "Database Administrator")
}
BiRel(user1,vpn_server, "User connects to VPN into office_network")
BiRel(vpn_server,_api_user_add, "/api/user/add accessed from the VPN server")
BiRel(vpn_server,_api_user, "/api/user accessed from the VPN server")
BiRel(_api_user_add,staging, "/api/user/add and adds data in the staging database")
BiRel(_api_user,staging, "/api/user gets data from the staging database")
@enduml
```


## Configuration

Configuration defines characteristics of a given resource. Default settings for a given resource type can be set in 
`./docs/defaults.yaml` as follows (following the same format for a resource type).

These settings will be applied to all resources generated. 

```
databases:
  audit_logging_alerts: true
  audit_logging_enabled: true
  audit_logging_monitored: true
  audit_logging_tamper_proof: true
  audit_logging_to_siem: true
  authentication_required: true
  automatic_updates: true
  cleanup_tasks_configured: true
  contains_pii: true
  database_os: MySQL
  default_accounts_enabled: true
  firewall_restricted: true
  has_scheduled_backup: true
  incident_response_runbooks: true
  is_encrypted: true
  is_hardened: true
  is_replica: true
  least_privileged_access: true
  least_privileged_network: true
  least_privileged_users: true
  passwords_hashed: true
  requires_encrypted_connections: true
  secure_logging_enabled: true
  tested_recovery_process: true
networks:
  has_wifi: false
  is_cloud: false
  is_public: false
systems:
  access_logging_enabled: true
  allows_manual_changes: true
  audit_logging_alerts: true
  audit_logging_enabled: true
  audit_logging_includes_user_details: true
  audit_logging_monitored: true
  audit_logging_tamper_proof: true
  audit_logging_to_siem: true
  authentication_required: true
  automatic_updates: true
  code_review_required: true
  code_scan_in_pipeline: true
  cors_minimal_required_usage: true
  db_op: true
  default_accounts_enabled: true
  delayed_login_failures: true
  dependabot_used: true
  dependency_signing_required: true
  has_secure_password_policy: true
  has_waf: true
  incident_response_runbooks: true
  input_sanitization: true
  input_validation: true
  ip_restrictions: true
  is_hardened: true
  least_privileged_access: true
  least_privileged_network: true
  login_failures_logged: true
  mfa_enabled: true
  password_username_incorrect_same_message: true
  public_facing: true
  requires_authentication: true
  requires_encryption: true
  secret_scanning_used: true
  secure_logging_enabled: true
  security_scan_on_artifact_storage: true
  security_scan_on_build: true
  sessions_stored_securely: true
  stateful_sessions_invalidated: true
  tested_recovery_process: true
users:
  company_device: true
  company_user: true
  uses_mfa: true
  uses_own_login: true

```

Overides can be set on a per-resource basis, by appending `configs` nested dictionary to the resources.yaml. The yaml 
below is based on having `"is_cloud": false` as a default setting - It will create two networks, one with is_cloud set
to `false` (the default), the other (`aws_public_subnet`) will have `is_cloud` set to `true`.


```
---
resources:
  networks:
    - name: office_network
    - name: aws_public_subnet
      - config:
        is_cloud: true
```

## Security Checks

Security checks have been included to cover use cases for the Owasp top 10, however you may want to extend pytmac with custom checks can be written and added to `./docs/security_checks.yaml`. These files should be written as below, the 
checks are iterated over and executed individually, all fields are required.

Severity should be used as a combination of Risk vs Likelihood, any security findings are prioritised by severity in the report output. 

```
user_owned_device:
  name: Non company device used
  description: Checks for users with company_user true and company_device false.
  remediation: Understand and remediate or document known exception.
  severity: 3
  resource_scope:
    - users
  check_query:
    - resources[resource]["company_user"] and not resources[resource]["company_device"]
```

## Outputs

The primary output of pytmac is a generated Markdown report, including a DFD (Data Flow Diagram) generated from the 
provided resources, and a programmatically generated list of security concerns using fields from the configuration
(including overrides).

Additionally, a yaml report is generated of all resources and their config - To ease reviewing the findings during a 
threat modelling session.
