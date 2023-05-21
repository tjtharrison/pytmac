[![FOSSA Status](https://app.fossa.com/api/projects/custom%2B37707%2Fgit%40github.com%3Atjtharrison%2Ftmac.git.svg?type=shield)](https://app.fossa.com/projects/custom%2B37707%2Fgit%40github.com%3Atjtharrison%2Ftmac.git?ref=badge_shield)
![Workflow Actionlint](https://github.com/tjtharrison/pytmac/actions/workflows/pr-actionlint.yaml/badge.svg)
![Workflow Checkov](https://github.com/tjtharrison/pytmac/actions/workflows/pr-checkov.yaml/badge.svg)
![Workflow Linting](https://github.com/tjtharrison/pytmac/actions/workflows/pr-linting.yaml/badge.svg)
![Workflow Unit Tests](https://github.com/tjtharrison/pytmac/actions/workflows/pr-tests.yaml/badge.svg)
![Workflow CodeQL](https://github.com/tjtharrison/pytmac/actions/workflows/pr-codeql.yaml/badge.svg)

[![PyPI version](https://badge.fury.io/py/pytmac.svg)](https://badge.fury.io/py/pytmac)
[![PyPI download month](https://img.shields.io/pypi/dm/pytmac.svg)](https://pypi.python.org/pypi/pytmac/)
[![PyPI download week](https://img.shields.io/pypi/dw/pytmac.svg)](https://pypi.python.org/pypi/pytmac/)
[![PyPI download day](https://img.shields.io/pypi/dd/pytmac.svg)](https://pypi.python.org/pypi/pytmac/)

# pytmac

Python based threat modelling as code tool (Python T.M.A.C).

# Installation

pytmac is available via PyPi, and can be installed with pip:

```
pip3 install pytmac
```

In order for DFD diagrams to be generated, [plantuml](https://plantuml.com/) must be installed on the system. If it is not installed, pytmac will continue to execute but the output will not include a DFD diagram.

# Usage

Once installed, pytmac can be called from the command line with an array of arguments which are described in the help page:

```
pytmac --help

options:
  -h, --help            show this help message and exit
  --version             Option to print the current version only
  --demo                Run pytmac in demo mode using the demo config and resources
  --output-dir OUTPUT_DIR
                        [Default: reports] Set the directory for report output
  --resources-file RESOURCES_FILE
                        The path to the resources file
  --config-file CONFIG_FILE
                        The path to the config file
  --defaults-file DEFAULTS_FILE
                        The path to the defaults file
  --security-checks-file SECURITY_CHECKS_FILE
                        [Default: security_checks.yaml] The path to the security-checks file
  --swagger-file SWAGGER_FILE
                        [Default: None] The path to the swagger file (optional)
```

## Demonstration

To generate an example report based on some pre-defined resources, run the following command:

```
pytmac --demo
```

This will write to a file called `report-[today-date].md` which can be viewed in a markdown viewer.

# Configuration

## Resources

Resources are defined as any asset that is part of the system being modelled under the following categories:

- Databases
- Networks
- Systems
- Users

Resources are provided to pytmac in a yaml file, which can be passed with the `--resources-file` argument. 

An example of a `resources.yaml` can be found in the pytmac repository at `./docs/resources.yaml`.

Resource config defines characteristics of a given resource. Default settings for a given resource type can be set in 
the resource yaml as follows (following the same format for a resource type).

```
resources:
  networks:
    - name: office_network
    - name: aws_public_subnet
      - config:
        is_cloud: true
```

## Defaults

Defaults are defined as any setting that is common across all resources. These are provided to pytmac in a yaml file, which can be passed with the `--defaults-file` argument.

An example of a `defaults.yaml` can be found in the pytmac repository at `./docs/defaults.yaml`.

Defaults can be overridden by resource config, and are applied to all resources unless overridden.

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
