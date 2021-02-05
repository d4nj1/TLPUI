
import re
from io import open
from json import load


def get_json_schema_object_from_file(objectname: str, filename: str) -> dict:
    jsonfile = open(filename)
    jsonobject = load(jsonfile)
    jsonfile.close()
    return jsonobject[objectname]


class TlpDefaults:
    def __init__(self, name: str, value: str, enabled: bool):
        self.name = name
        self.value = value
        self.enabled = enabled

    def get_name(self) -> str:
        return self.name

    def get_value(self) -> str:
        return self.value

    def is_enabled(self) -> bool:
        return self.enabled


def extract_default_tlp_configs(filename: str) -> dict:
    propertypattern = re.compile(r'^#?[A-Z_\d]+=')
    fileopener = open(filename)
    lines = fileopener.readlines()
    fileopener.close()

    tlpconfig_defaults = dict()
    for line in lines:
        if propertypattern.match(line):
            cleanline = line.lstrip().rstrip()

            if (cleanline.startswith('#')):
                enabled = False
                cleanline = cleanline.lstrip('#')
            else:
                enabled = True

            property = cleanline.split('=', maxsplit=1)
            propertyname = property[0]
            propertyvalue = property[1]

            if propertyvalue.startswith('\"') and propertyvalue.endswith('\"'):
                propertyvalue = propertyvalue.lstrip('\"').rstrip('\"')

            tlpconfig_defaults[propertyname] = TlpDefaults(propertyname, propertyvalue, enabled)
    return tlpconfig_defaults
