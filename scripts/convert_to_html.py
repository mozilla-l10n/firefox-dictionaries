#! /usr/bin/env python3

import os
import json


def main():
    script_folder = os.path.abspath(os.path.dirname(__file__))

    # Curated list

    # Read JSON data
    file_name = os.path.join(
        script_folder, os.path.pardir, 'output', 'dictionaries_curated.json')
    with open(file_name) as inputfile:
        curated_data = json.load(inputfile)

    # Read HTML template
    file_name = os.path.join(
        script_folder, os.path.pardir, 'templates', 'curated.html')
    with open(file_name) as inputfile:
        template = inputfile.read()

    tbl_content = []
    for locale_code, locale_data in curated_data.items():
        tbl_content.append('''
            <tr>
                <th scope="row" rowspan="{}">{}</th>'''.format(
                                                            len(locale_data),
                                                            locale_code))

        first_dictionary = True
        for dictionary in locale_data:
            if not first_dictionary:
                tbl_content.append('<tr>\n')

            tbl_content.append('''
                <td>{}</td>
                <td>{}</td>
                <td><a href="{}">{}</a></td>
            </tr>'''.format(
                        dictionary['locale'],
                        dictionary['guid'],
                        dictionary['url'],
                        dictionary['name']))
            first_dictionary = False

    # Write HTML output
    template = template.replace('%TABLEBODY%', '\n'.join(tbl_content))
    file_name = os.path.join(
        script_folder, os.path.pardir, 'pages', 'index.html')
    with open(file_name, 'w') as outputfile:
        outputfile.write(template)

    # Complete list
    # Read JSON data
    file_name = os.path.join(
        script_folder, os.path.pardir, 'output', 'dictionaries_complete.json')
    with open(file_name) as inputfile:
        full_data = json.load(inputfile)

    # Read HTML template
    file_name = os.path.join(
        script_folder, os.path.pardir, 'templates', 'complete.html')
    with open(file_name) as inputfile:
        template = inputfile.read()

    tbl_content = []
    for locale_code, locale_data in full_data['list'].items():
        tbl_content.append('''
            <tr>
                <th scope="row" rowspan="{}">{}</th>'''.format(
            len(locale_data),
            locale_code))

        first_dictionary = True
        for dictionary in locale_data:
            if not first_dictionary:
                tbl_content.append('<tr>\n')

            tbl_content.append('''
                <td>{}</td>
                <td>{}</td>
                <td><a href="{}">{}</a></td>
            </tr>'''.format(
                dictionary['locale'],
                dictionary['guid'],
                dictionary['url'],
                dictionary['name']))
            first_dictionary = False

    multi_content = []
    multi_dictionaries = full_data['stats']['multi']
    locales = list(multi_dictionaries.keys())
    locales.sort()
    for locale in locales:
        multi_content.append(
            '<li>{}: {}</li>'.format(locale, multi_dictionaries[locale]))

    # Write HTML output
    template = template.replace('%TOTAL%', str(full_data['stats']['total']))
    template = template.replace(
        '%IGNORED%', str(full_data['stats']['ignored']))
    template = template.replace('%MULTI%', '\n'.join(multi_content))
    template = template.replace('%TABLEBODY%', '\n'.join(tbl_content))
    file_name = os.path.join(
        script_folder, os.path.pardir, 'pages', 'complete.html')
    with open(file_name, 'w') as outputfile:
        outputfile.write(template)


if __name__ == '__main__':
    main()
