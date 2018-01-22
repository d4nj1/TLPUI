from io import open
import os

from file import get_json_schema_object_from_file


lastvalue = ''

def add_to_list(listobject: list, value: str):
    global lastvalue
    if not value in listobject:
        if lastvalue in listobject:
            lastindex = listobject.index(lastvalue)
            listobject.insert(lastindex+1, value)
        else:
            listobject.append(value)

    lastvalue = value


def create_translateable_strings_header_file():
    """ This method extracts items for translation from configschema.json and puts them in new file with
    header extension (.h) because poedit and other po-tools do not support JSON files right now. This method
    should be called any time configschema.json changes and translation needs to be updated.
    Change configschema.json -> run this script -> update po files from source with utility (e.g. poedit)"""

    translateobjects = list()

    for file in os.listdir('../configschema'):
        if not file.endswith('.json'):
            continue

        categories = get_json_schema_object_from_file('categories', '../configschema/' + file)

        for category in categories:
            add_to_list(translateobjects, category['name'] + '__CATEGORY_TITLE')
            configs = category['configs']
            for config in configs:
                if 'group' in config:
                    add_to_list(translateobjects, config['group'] + '__GROUP_TITLE')
                    add_to_list(translateobjects, config['group'] + '__GROUP_DESCRIPTION')
                    configitems = config['ids']
                    for configitem in configitems:
                        add_to_list(translateobjects, configitem['id'] + '__ID_TITLE')
                else:
                    add_to_list(translateobjects, config['id'] + '__ID_TITLE')
                    add_to_list(translateobjects, config['id'] + '__ID_DESCRIPTION')


    newfile = open('configschema.json.h', 'w+')
    for item in translateobjects:
        newfile.write('_(\"' + item + '\");\n')
    newfile.close()


create_translateable_strings_header_file()
