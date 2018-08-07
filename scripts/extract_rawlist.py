#! /usr/bin/env python3

from urllib.request import urlopen
import json
import os
import sys


def getShippingLocales():
    # Get the list of locales shipping in Firefox
    base = 'https://hg.mozilla.org/mozilla-central/raw-file/default/{}'
    locales_urls = [
        base.format('browser/locales/all-locales'),
        base.format('mobile/android/locales/all-locales'),
    ]

    shipping_locales = []
    for locales_url in locales_urls:
        try:
            with urlopen(locales_url) as response:
                output = response.readlines()
                for locale in output:
                    locale = locale.rstrip().decode()
                    shipping_locales.append(locale)
        except Exception as e:
            print(e)

    shipping_locales = list(set(shipping_locales))
    shipping_locales.sort()

    return shipping_locales


def main():
    # Get the list of supported locales in Firefox and Firefox for Android
    locales = getShippingLocales()

    # Get the list of dictionaries available on AMO
    try:
        dictionaries = {
            'list': {},
            'stats': {},
        }
        url = ('https://addons.mozilla.org/api/v3/addons/language-tools/'
               '?app=firefox&type=dictionary')
        response = urlopen(url)
        json_data = json.load(response)
    except Exception as e:
        print(e)
        sys.exit(1)

    ignored_dictionaries = []
    for dictionary in json_data['results']:
        locale = dictionary['target_locale']
        supported_locale = True

        if locale not in locales:
            # e.g. include 'de-DE' in 'de'
            if locale.split('-')[0] not in locales:
                ignored_dictionaries.append(dictionary['guid'])
                supported_locale = False
            else:
                locale = locale.split('-')[0]

        if supported_locale:
            if locale not in dictionaries['list']:
                dictionaries['list'][locale] = []
            name = (dictionary['name']['en-US']
                    if 'en-US' in dictionary['name']
                    else list(dictionary['name'].values())[0])
            dictionaries['list'][locale].append(
                {
                    'guid': dictionary['guid'],
                    'locale': dictionary['target_locale'],
                    'name': name,
                    'url': dictionary['url'].replace('/en-US/', '/'),
                })

    # Store stats and output them
    print('Total dictionaries: {}'.format(len(json_data['results'])))
    print('Ignored dictionaries: {}'.format(len(ignored_dictionaries)))

    multi_dictionaries = {}
    for locale, locale_data in dictionaries['list'].items():
        if len(locale_data) > 1:
            multi_dictionaries[locale] = len(locale_data)

    if multi_dictionaries:
        print('Locales with more than one dictionary:')
        locales = list(multi_dictionaries.keys())
        locales.sort()
        for locale in locales:
            print('  {}: {}'.format(locale, multi_dictionaries[locale]))

    dictionaries['stats'] = {
        'total': len(json_data['results']),
        'ignored': len(ignored_dictionaries),
        'multi': multi_dictionaries,
    }

    # Store the file
    script_folder = os.path.abspath(os.path.dirname(__file__))
    file_name = os.path.join(
        script_folder, os.path.pardir, 'output', 'dictionaries_full.json')
    with open(file_name, 'w') as outfile:
        json.dump(dictionaries, outfile, indent=2, sort_keys=True)


if __name__ == '__main__':
    main()
