"""This module provides helper functions for refreshing config PO files."""

import os
from io import open
from tlpui.filehelper import get_yaml_schema_object_from_file

lastvalue = ''


def add_to_list(listobject: list, value: str):
    """Add values to list."""
    global lastvalue
    if value not in listobject:
        if lastvalue in listobject:
            lastindex = listobject.index(lastvalue)
            listobject.insert(lastindex + 1, value)
        else:
            listobject.append(value)

    lastvalue = value


def create_translateable_strings_header_file():
    """Extract translation items from configschema/*.yaml and put them into a new file with header extension.

    Poedit and other po-tools do not support YAML files right now.
    It should be called any time yaml files get added or updated.

    Update or add VERSION.yaml -> run this script -> update po files from header source with utility (e.g. poedit).
    """
    translateobjects = list()

    for file in os.listdir('tlpui/configschema'):
        if not file.endswith('.yaml'):
            continue

        categories = get_yaml_schema_object_from_file('categories', 'tlpui/configschema/' + file)

        for category in categories:
            add_to_list(translateobjects, category['name'] + '__CATEGORY_TITLE')
            configs = category['configs']
            for config in configs:
                if 'group' in config:
                    # add_to_list(translateobjects, config['group'] + '__GROUP_TITLE')
                    add_to_list(translateobjects, config['group'] + '__GROUP_DESCRIPTION')
                    # configitems = config['ids']
                    # for configitem in configitems:
                    #    add_to_list(translateobjects, configitem['id'] + '__ID_TITLE')
                else:
                    # add_to_list(translateobjects, config['id'] + '__ID_TITLE')
                    add_to_list(translateobjects, config['id'] + '__ID_DESCRIPTION')

    newfile = open('tlpui/lang/configschema.yaml.h', 'w+')
    for item in translateobjects:
        newfile.write('_(\"' + item + '\");\n')
    newfile.close()


create_translateable_strings_header_file()
