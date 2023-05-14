import json
import os
from datetime import date

import pytest

import tests.bin.dirs as dirs
from bin import get_config as get_config

OUTPUT_REPORT_DIRECTORY = os.environ.get("OUTPUT_DIR")
OUTPUT_REPORT_FILE = OUTPUT_REPORT_DIRECTORY + "/report-" + str(date.today()) + ".md"
CONFIG_FILE = os.environ.get("CONFIG_FILE")

import tmac

RESOURCES_FILE = "tests/docs/test_resources.yaml"
CONFIG_FILE = "tests/docs/test_config.yaml"
DEFAULTS_FILE = "docs/defaults.yaml"
OUTPUT_DIR = "tests/reports"
SECURITY_CHECKS_FILE = "docs/security_checks.yaml"
SWAGGER_FILE = "docs/swagger.json"
OUTPUT_REPORT_FILE = OUTPUT_DIR + "/report-" + str(date.today()) + ".md"

security_checks_input = get_config.security_checks(SECURITY_CHECKS_FILE)
resources_input = get_config.resources(RESOURCES_FILE)
config_input = get_config.config(CONFIG_FILE)
defaults_input = get_config.defaults(DEFAULTS_FILE)
swagger_input = get_config.swagger(SWAGGER_FILE)


@pytest.fixture(autouse=True)
def my_fixture():
    """
    Wrapper for config unit tests to back up and restore configuration to test field manipulation.
    :return:
    """
    dirs.create()
    yield


def test_report_contents():
    """
    Function to verify the report contents line by line, also checking indentation
    :return: True/False
    """
    output_valid = True
    tmac.main(
        resources_input,
        config_input,
        defaults_input,
        security_checks_input,
        OUTPUT_DIR,
        swagger_input,
    )

    with open(OUTPUT_REPORT_FILE, "r") as markdown_file:
        markdown_file_contents = markdown_file.readlines()

    new_list = []

    for line in markdown_file_contents:
        line = line.replace("\n", "")
        if len(line) > 0:
            new_list.append(
                {
                    "name": line.replace("\t", ""),
                    "level": line.count("\t"),
                }
            )

    # Set some checks to `False` to be corrected if values present  and correct
    title_correct = False
    description_correct = False
    mermaid_prefix_correct = False
    mermaid_suffix_correct = False
    mermaid_type_correct = False
    boundary_correct = False
    person_correct = False
    db_correct = False
    system_correct = False
    relationship_correct = False
    diagram_correct = False

    for line in new_list:
        print(line)
        if line["name"] == "# tmac" and line["level"] == 0:
            title_correct = True

        if (
            line["name"]
            == "This is an example of how tmac can be used to threat model your workload"
            and line["level"] == 0
        ):
            description_correct = True

        if line["name"] == "```plantuml" and line["level"] == 0:
            mermaid_prefix_correct = True

        if line["name"] == "```" and line["level"] == 0:
            mermaid_suffix_correct = True

        if (
            line["name"] == "@startuml report-" + str(date.today())
            and line["level"] == 0
        ):
            mermaid_type_correct = True

        if (
            line["name"] == 'Boundary(bhome_network, "home_network") {'
            and line["level"] == 0
        ):
            boundary_correct = True

        if (
            line["name"] == 'Person(test_user, "test_user", "Testing user")'
            and line["level"] == 1
        ):
            person_correct = True

        if (
            line["name"]
            == 'SystemDb(test_database,"test_database ", "Testing database")'
            and line["level"] == 1
        ):
            db_correct = True

        if (
            line["name"] == 'System(test_system,"test_system ", "Testing system")'
            and line["level"] == 1
        ):
            system_correct = True

        if (
            line["name"]
            == 'BiRel(test_user,test_system, "Test connection from user to system")'
            and line["level"] == 0
        ):
            relationship_correct = True

        if (
            line["name"] == "![Diagram](./report-" + str(date.today()) + ".svg)"
            and line["level"] == 0
        ):
            diagram_correct = True

    for check in [
        mermaid_type_correct,
        boundary_correct,
        title_correct,
        description_correct,
        mermaid_prefix_correct,
        mermaid_suffix_correct,
        person_correct,
        db_correct,
        system_correct,
        relationship_correct,
        diagram_correct,
    ]:
        if check == False:
            print(str(check) + " has failed")
            assert False
        else:
            print("PASS - " + str(check))

    assert True


#### Need to test insecure resource
# def test_insecure_resource_table():

#### Need to test multiple insecure resource sorting (by severity)
# def test_multiple_insecure_order():

### Need to validate defaults input (min required)

### Need to validate config input (min required)

### Need to validate resources input (min required)
