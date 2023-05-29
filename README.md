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
```

## Demonstration

To generate an example report based on some pre-defined resources, run the following command:

```
pytmac --demo
```

This will write to a file called `report-[today-date].md` which can be viewed in a markdown viewer.

# Configuration

## Init mode

pytmac can be run in init mode to generate configuration files using a combination of inputs provided and default project settings. This can be done with the following command:

```bash
pytmac --init
```

Once the initialisation has completed, you should review the generated files and make any changes required (Primary focus should be on the defaults file as this will globally define security settings for all generated resources in your project.

## Config file

pytmac on launch will look for a file in the current directory named `.pytmac` as a source of settings. This file can be used to set the following settings:

```
resource_file: "docs/resources.yaml"
config_file: "docs/config.yaml"
defaults_file: "docs/defaults.yaml"
```

If both a config file value and a manual override is added via the command line, the command line value will take precedence.

Eg if you have a .pytmac file with the following:

```
resource_file: "docs/resources.yaml"
```

and call pytmac with the following:

```
pytmac --resources-file resources.yaml
```

the resources.yaml file will be used over the one defined in the .pytmac file.

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

# Release Details

This project uses [semantic versioning](https://semver.org/) for releases, which are determined and managed by [python-semantic-release](https://python-semantic-release.readthedocs.io/en/latest/). 

Python-semantic-release relies on conventional commits being used for all commit messages to determine the next version number / semantic release type (major/minor/patch).

Once the new version number has been determined, a new release is created on github, and the new version is published to PyPi.

## gpush

You can use my other project [gpush](https://github.com/tjtharrison/gpush) to ensure you always push commits with the correct format for this project, otherwise, details on commit message structure can be found on the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) website.
