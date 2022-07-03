#! /usr/bin/env python3

import os
import json
from bs4 import BeautifulSoup as bs


def populateTable(data):
    tbl_content = []
    for locale_code, locale_data in data.items():
        tbl_content.append(
            f'<tr><th scope="row" rowspan="{len(locale_data)}">{locale_code}</th>'
        )

        first_dictionary = True
        for dictionary in locale_data:
            if not first_dictionary:
                tbl_content.append("<tr>")

            tbl_content.append(
                f"""
                <td>{dictionary["locale"]}</td>
                <td>{dictionary["guid"]}</td>
                <td><a href="{dictionary["url"]}">{dictionary["name"]}</a></td>
            </tr>"""
            )
            first_dictionary = False

    return tbl_content


def writeHTML(content, file_name):
    # Prettify HTML
    soup = bs(content)
    pretty_content = soup.prettify()

    with open(file_name, "w") as outputfile:
        outputfile.write(pretty_content)


def main():
    script_folder = os.path.abspath(os.path.dirname(__file__))

    # Curated list

    # Read JSON data
    file_name = os.path.join(
        script_folder, os.path.pardir, "output", "dictionaries_curated.json"
    )
    with open(file_name) as inputfile:
        curated_data = json.load(inputfile)

    # Read HTML template
    file_name = os.path.join(script_folder, os.path.pardir, "templates", "curated.html")
    with open(file_name) as inputfile:
        template = inputfile.read()

    tbl_content = populateTable(curated_data)

    # Write HTML output
    template = template.replace("%TABLEBODY%", "\n".join(tbl_content))
    file_name = os.path.join(script_folder, os.path.pardir, "docs", "index.html")
    writeHTML(template, file_name)

    # Complete list
    # Read JSON data
    file_name = os.path.join(
        script_folder, os.path.pardir, "output", "dictionaries_complete.json"
    )
    with open(file_name) as inputfile:
        full_data = json.load(inputfile)

    # Read HTML template
    file_name = os.path.join(
        script_folder, os.path.pardir, "templates", "complete.html"
    )
    with open(file_name) as inputfile:
        template = inputfile.read()

    tbl_content = populateTable(full_data["list"])

    multi_content = []
    multi_dictionaries = full_data["stats"]["multi"]
    locales = list(multi_dictionaries.keys())
    locales.sort()
    for locale in locales:
        multi_content.append(f"<li>{locale}: {multi_dictionaries[locale]}</li>")

    # Write HTML output
    template = template.replace("%TOTAL%", str(full_data["stats"]["total"]))
    template = template.replace("%IGNORED%", str(full_data["stats"]["ignored"]))
    template = template.replace("%MULTI%", "\n".join(multi_content))
    template = template.replace("%TABLEBODY%", "\n".join(tbl_content))
    file_name = os.path.join(script_folder, os.path.pardir, "docs", "complete.html")
    writeHTML(template, file_name)


if __name__ == "__main__":
    main()
