import re
from os import path
from io import open
from json import load
from os import remove, close, path
from shutil import move
from tempfile import mkstemp

from config import TlpConfig


cwd = path.dirname(path.abspath(__file__)) + '/'

def get_json_schema_object(objectname) -> dict:
    tlpprovidedschema = '/usr/share/tlp-pm/configschema.json'
    if path.exists(tlpprovidedschema):
        return get_json_schema_object_from_file(objectname, tlpprovidedschema)
    else:
        return get_json_schema_object_from_file(objectname, cwd + 'configschema.json')


def get_json_schema_object_from_file(objectname, filename) -> dict:
    jsonfile = open(filename)
    jsonobject = load(jsonfile)
    return jsonobject[objectname]


def read_tlp_file_config(filename) -> dict:
    propertypattern = re.compile('^#?[A-Z_\d]+=')
    fileproperties = dict()
    fileopener = open(filename)
    lines = fileopener.readlines()
    fileopener.close()
    linenumber = 0

    for line in lines:
        linenumber += 1
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
                isquoted = True
                propertyvalue = propertyvalue.lstrip('\"').rstrip('\"')
            else:
                isquoted = False

            fileproperties[propertyname] = TlpConfig(line, linenumber, enabled, propertyname, propertyvalue, isquoted)

    return fileproperties


def write_tlp_file_config(changedproperties, filename):
    fh, tmpfilename = mkstemp()
    newfile = open(tmpfilename, 'w')

    oldfile = open(filename)
    lines = oldfile.readlines()
    oldfile.close()

    linenumber = 0

    for line in lines:
        linenumber += 1
        changedline = False

        for property in changedproperties:
            if line == property[0] and linenumber == property[1]:
                newfile.write(property[2] + '\n')
                changedline = True
                break

        if not changedline:
            newfile.write(line)

    newfile.close()
    close(fh)
    oldfile.close()

    remove(filename)
    move(tmpfilename, filename)
