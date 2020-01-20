import re
from subprocess import check_output
from io import open
from json import load
from os import access, W_OK, close, path
from tempfile import mkstemp
from .config import TlpConfig
from . import settings
from .uihelper import get_graphical_sudo, SUDO_MISSING_TEXT


def get_json_schema_object(objectname) -> dict:
    tlpprovidedschema = '/usr/share/tlp-pm/configschema.json'
    if path.exists(tlpprovidedschema):
        return get_json_schema_object_from_file(objectname, tlpprovidedschema)
    else:
        majorminor = settings.get_installed_major_minor_version()
        return get_json_schema_object_from_file(objectname, settings.workdir + '/configschema/' + majorminor + '.json')


def get_json_schema_object_from_file(objectname: str, filename: str) -> dict:
    jsonfile = open(filename)
    jsonobject = load(jsonfile)
    jsonfile.close()
    return jsonobject[objectname]


def read_tlp_file_config(filename) -> dict:
    propertypattern = re.compile(r'^#?[A-Z_\d]+=')
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


def create_tmp_tlp_config_file(changedproperties):
    fh, tmpfilename = mkstemp()
    newfile = open(tmpfilename, 'w')

    oldfile = open(settings.tlpconfigfile)
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

    return tmpfilename


def write_tlp_config(tmpconfigfile: str) -> str:
    sedtlpconfigfile = "w" + settings.tlpconfigfile

    if access(settings.tlpconfigfile, W_OK):
        check_output(["sed", "-n", sedtlpconfigfile, tmpconfigfile])
        return ''
    else:
        sudo_cmd = get_graphical_sudo()

        if sudo_cmd is None:
            return SUDO_MISSING_TEXT

        check_output([sudo_cmd, "sed", "-n", sedtlpconfigfile, tmpconfigfile])
        return ''
