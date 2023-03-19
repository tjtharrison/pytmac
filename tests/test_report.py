import json
import os
from datetime import date
import main
import pytest

OUTPUT_REPORT_DIRECTORY = os.environ.get("OUTPUT_DIR")
OUTPUT_REPORT_FILE = OUTPUT_REPORT_DIRECTORY + "/report-" + str(date.today()) + ".md"
CONFIG_FILE = os.environ.get("CONFIG_FILE")

import main


def test_report_contents():
    """
    Function to verify the report contents line by line, also checking indentation
    :return: True/False
    """
    output_valid = True
    main.main()

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

    print(json.dumps(new_list))
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
    container_correct = False
    relationship_correct = False

    for line in new_list:
        if line["name"] == "# test_doc" and line["level"] == 0:
            title_correct = True

        if line["name"] == "Threat modelling for testing" and line["level"] == 0:
            description_correct = True

        if line["name"] == "```plantuml" and line["level"] == 0:
            mermaid_prefix_correct = True

        if line["name"] == "```" and line["level"] == 0:
            mermaid_suffix_correct = True

        if (
            line["name"] == "@startuml Threat modelling for testing"
            and line["level"] == 0
        ):
            mermaid_type_correct = True

        if (
            line["name"] == 'Boundary(btest_network, "test_network") {'
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
            line["name"] == 'System(test_system,"test_system ", "Test System")'
            and line["level"] == 1
        ):
            system_correct = True

        if (
            line["name"]
            == 'Container(test_container,"test_container ", "Testing Container")'
            and line["level"] == 1
        ):
            container_correct = True

        if (
            line["name"]
            == 'BiRel(test_user,test_system, "Test connection from user to system")'
            and line["level"] == 1
        ):
            relationship_correct = True

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
        container_correct,
        relationship_correct,
    ]:
        if check == False:
            assert False
            print(check + " has failed")
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
