#!/usr/bin/env python3
"""Generate mkgendocs.yaml from python files by iterating over files and functions."""

import os
import yaml


def get_mkgendocs_config():
    """
    Get the mkgendocs configuration file.

    Raises:
        FileNotFoundError: If mkgendocs.yaml is not found
        YAMLError: If there is an error parsing mkgendocs.yaml

    Returns:
        mkgendocs configuration

    """
    try:
        with open("mkgendocs.yaml") as mkgendocs_config:
            return yaml.safe_load(mkgendocs_config)
    except FileNotFoundError:
        print("mkgendocs.yaml not found")
        raise FileNotFoundError
    except yaml.YAMLError as error_message:
        raise yaml.YAMLError() from error_message


# Function to get a list of python files in a directory
def get_python_files(directory):
    """
    Get a list of python files in a directory.

    Args:
        directory: Directory to search

    Returns:
        List of python files
    """
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and (
                not root.startswith("./tests")
                and not file.startswith("_")
                and not root.startswith("./build")
            ):
                python_files.append(os.path.join(root, file))
    return python_files


def get_file_functions(filename):
    """
    Get the functions in a file.

    Args:
        filename: The name of the file to parse for functions.

    Returns:
        List of functions

    """
    with open(filename) as file:
        lines = file.readlines()
    functions = []
    for line in lines:
        if line.startswith("def"):
            functions.append(line.split(" ")[1].split("(")[0])
    return functions


def main():
    """Generate configuration for mkgendocs to build documentation."""
    print("Starting doc generation")
    mkgendocs_config = get_mkgendocs_config()
    new_pages = []

    print("Getting a list of functions in python files..")
    python_files = get_python_files(".")
    for python_file in python_files:
        functions = get_file_functions(python_file)
        if len(functions) > 0:
            print("Functions found, adding " + python_file)
            new_pages.append(
                {
                    "page": python_file.replace(".py", ".md").replace("./", ""),
                    "source": python_file,
                    "functions": functions,
                }
            )
        else:
            print("No functions found, skipping " + python_file)

    mkgendocs_config["pages"] = new_pages

    with open("mkgendocs.yaml", "w") as mkgendocs_config_file:
        yaml.dump(mkgendocs_config, mkgendocs_config_file)


if __name__ == "__main__":
    main()
