from io import open

from file import get_json_schema_object_from_file


def create_translateable_strings_header_file():
    categories = get_json_schema_object_from_file('categories', '../configschema.json')
    newfile = open('configschema.json.h', 'w+')

    for category in categories:
        configs = category['configs']
        newfile.write('_(\"' + category['name'] + '_CATEGORY\");\n')
        for config in configs:
            if 'group' in config:
                descriptiontag = config['group'] + '_GROUP'
            else:
                descriptiontag = config['id'] + '_ID'
            newfile.write('_(\"' + descriptiontag + '\");\n')

    newfile.close()


create_translateable_strings_header_file()
