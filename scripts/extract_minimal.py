#! /usr/bin/env python3

import json
import os


def main():
    script_folder = os.path.abspath(os.path.dirname(__file__))

    # Read JSON data
    file_name = os.path.join(
        script_folder, os.path.pardir, "output", "dictionaries_curated.json"
    )
    with open(file_name) as inputfile:
        curated_data = json.load(inputfile)

    minimal_data = {}
    for locale_code, locale_data in curated_data.items():
        minimal_data[locale_code] = []
        for dictionary in locale_data:
            minimal_data[locale_code].append(dictionary["guid"])

    # Write JSON data
    file_name = os.path.join(
        script_folder, os.path.pardir, "output", "dictionaries_minimal.json"
    )
    with open(file_name, "w") as outputfile:
        json.dump(minimal_data, outputfile, indent=2, sort_keys=True)


if __name__ == "__main__":
    main()
