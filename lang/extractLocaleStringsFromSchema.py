from io import open

from file import get_json_schema_object_from_file


def create_translateable_strings_header_file():
    """ This method extracts items for translation from configschema.json and puts them in new file with
    header extension (.h) because poedit and other po-tools do not support JSON files right now. This method
    should be called any time configschema.json changes and translation needs to be updated.
    Change configschema.json -> run this script -> update po files from source with utility (e.g. poedit)"""

    categories = get_json_schema_object_from_file('categories', '../configschema.json')
    newfile = open('configschema.json.h', 'w+')

    for category in categories:
        newfile.write('_(\"' + category['name'] + '_CATEGORY\");\n')
        configs = category['configs']
        for config in configs:
            if 'group' in config:
                descriptiontag = config['group'] + '_GROUP'
            else:
                descriptiontag = config['id'] + '_ID'
            newfile.write('_(\"' + descriptiontag + '\");\n')

    newfile.close()


create_translateable_strings_header_file()
