import json
from datetime import date

date_today = str(date.today())

with open("docs/resources.json", "r") as resources_file:
    resources_json = json.loads(resources_file.read())

with open("docs/config.json", "r") as config_file:
    config_json = json.loads(config_file.read())

resources = resources_json["resources"]

with open("reports/report-" + date_today + ".md", "w", encoding="UTF-8") as output_file:
    # Write intro
    output_file.write("# " + config_json["title"] + "\n")
    for description_line in config_json["description"]:
        output_file.write(description_line + "\n\n")


    output_file.write("# Data Flow Diagram\n")
    output_file.write("```mermaid")
    output_file.write("\n")
    output_file.write("C4Context")
    output_file.write("\n")

    for network in resources["networks"]:
        output_file.write(
            "\t"
            + "System_Boundary(b"
            + network["name"]
            + ', "'
            + network["name"]
            + '") {'
            + "\n"
        )
        for user in resources["users"]:
            if user["network"] == network["name"]:
                output_file.write(
                    "\t\t"
                    + "Person("
                    + user["name"]
                    + ', "'
                    + user["name"]
                    + '", "'
                    + user["description"]
                    + '")'
                    + "\n"
                )

        for database in resources["databases"]:
            if database["network"] == network["name"]:
                output_file.write(
                    "\t\t"
                    + "SystemDb("
                    + database["name"]
                    + ","
                    + '"'
                    + database["name"]
                    + ' ", "'
                    + database["description"]
                    + '")'
                    + "\n"
                )

        for system in resources["systems"]:
            if system["network"] == network["name"]:
                output_file.write(
                    "\t\t"
                    + "System("
                    + system["name"]
                    + ","
                    + '"'
                    + system["name"]
                    + ' ", "'
                    + system["description"]
                    + '")'
                    + "\n"
                )
        output_file.write("\t" + "}" + "\n")

    for res_links in resources["res_links"]:
        output_file.write(
            "\t"
            + "BiRel("
            + res_links["source"]
            + ","
            + res_links["destination"]
            + ', "'
            + res_links["description"]
            + '")'
            + "\n"
        )
        output_file.write("\n")
    output_file.write("UpdateLayoutConfig($c4ShapeInRow=\"3\", $c4BoundaryInRow=\"1\")" + "\n")
    output_file.write("```")
