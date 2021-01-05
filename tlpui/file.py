import copy
import re
from sys import stdout
from subprocess import check_output, STDOUT
from io import open
from json import load
from os import access, W_OK, close, path
from tempfile import mkstemp
from .config import TlpDefaults, TlpConfig, ConfType
from . import settings
from .uihelper import get_graphical_sudo, SUDO_MISSING_TEXT


def get_json_schema_object(objectname) -> dict:
    tlpprovidedschema = '/usr/share/tlp-pm/configschema.json'
    if path.exists(tlpprovidedschema):
        return get_json_schema_object_from_file(objectname, tlpprovidedschema)
    else:
        majorminor = settings.tlpbaseversion
        return get_json_schema_object_from_file(objectname, settings.workdir + '/configschema/' + majorminor + '.json')


def get_json_schema_object_from_file(objectname: str, filename: str) -> dict:
    jsonfile = open(filename)
    jsonobject = load(jsonfile)
    jsonfile.close()
    return jsonobject[objectname]


def init_tlp_file_config() -> None:
    settings.tlpconfig = dict()
    tlpversion = settings.tlpbaseversion
    read_default_tlp_file_config('{}/defaults/tlp-{}.conf'.format(settings.workdir, tlpversion))

    if tlpversion not in ["0_8", "0_9", "1_0", "1_1", "1_2"]:
        # update default values with intrinsic ones
        intrinsic_defaults_path = f"{settings.folder_prefix}/usr/share/tlp/defaults.conf"
        read_default_tlp_file_config(intrinsic_defaults_path)

    # get current settings from tlp itself
    simple_stat_command = ["tlp-stat", "-c"]
    tlpstat = check_output(simple_stat_command, stderr=STDOUT).decode(stdout.encoding)
    tlpsettinglines = tlpstat.split('\n')

    if tlpversion in ["0_8", "0_9", "1_0", "1_1", "1_2"]:
        extract_tlp_settings_obsolete(tlpsettinglines)
    else:
        extract_tlp_settings(tlpsettinglines)

    # Add default tlp configs not set in current settings
    for key, default in settings.tlpconfig_defaults.items():     # type: TlpDefaults
        configname = default.get_name()
        if configname not in settings.tlpconfig.keys():
            enabled = default.is_enabled()
            value = default.get_value()
            settings.tlpconfig[configname] = TlpConfig(enabled, configname, value, ConfType.DEFAULT, "")

    # finally store copy for comparing changes
    settings.tlpconfig_original = copy.deepcopy(settings.tlpconfig)


def extract_tlp_settings_obsolete(lines: list) -> None:
    propertypattern = re.compile(r'^[A-Z_\d]+=')

    for line in lines:
        if propertypattern.match(line):
            cleanline = line.lstrip().rstrip()

            property = cleanline.split('=', maxsplit=1)
            propertyname = property[0]
            propertyvalue = property[1]

            if propertyvalue.startswith('\"') and propertyvalue.endswith('\"'):
                propertyvalue = propertyvalue.lstrip('\"').rstrip('\"')

            settings.tlpconfig[propertyname] = TlpConfig(True, propertyname, propertyvalue, ConfType.USER, settings.tlpconfigfile)


def extract_tlp_settings(lines: list) -> None:
    propertypattern = re.compile(r'^.+?\.conf\sL\d+\:\s[A-Z_\d]+=')

    for line in lines:
        if propertypattern.match(line):
            cleanline = line.lstrip().rstrip()
            settingsparts = cleanline.split(' ', maxsplit=2)
            configfile = settingsparts[0]       # type: str
            if configfile == 'defaults.conf':
                conftype = ConfType.DEFAULT
            elif configfile.startswith('/etc/tlp.d/'):
                conftype = ConfType.DROPIN
            elif configfile == "/etc/tlp.conf":
                conftype = ConfType.USER
            else:
                print('Config type not found for file: {}'.format(configfile))
                conftype = ConfType.ERR

            property = settingsparts[2].split('=', maxsplit=1)
            propertyname = property[0]
            propertyvalue = property[1]

            if propertyvalue.startswith('\"') and propertyvalue.endswith('\"'):
                propertyvalue = propertyvalue.lstrip('\"').rstrip('\"')

            settings.tlpconfig[propertyname] = TlpConfig(True, propertyname, propertyvalue, conftype, configfile)


def read_default_tlp_file_config(filename: str) -> None:
    propertypattern = re.compile(r'^#?[A-Z_\d]+=')
    fileopener = open(filename)
    lines = fileopener.readlines()
    fileopener.close()

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

            settings.tlpconfig_defaults[propertyname] = TlpDefaults(propertyname, propertyvalue, enabled)


def create_tmp_tlp_config_file(changedproperties: dict) -> str:
    propertypattern = re.compile(r'^#?[A-Z_\d]+=')
    fh, tmpfilename = mkstemp()
    newfile = open(tmpfilename, 'w')

    oldfile = open(settings.tlpconfigfile)
    lines = oldfile.readlines()
    oldfile.close()

    for line in lines:
        if propertypattern.match(line):
            cleanline = line.lstrip().lstrip('#')

            property = cleanline.split('=', maxsplit=1)
            propertyname = property[0]

            if propertyname in changedproperties.keys():
                if cleanline.startswith(propertyname + "="):
                    newfile.write(changedproperties[propertyname] + '\n')
                    continue

        newfile.write(line)

    newfile.close()
    close(fh)
    oldfile.close()

    return tmpfilename


def write_tlp_config(tmpconfigfile: str) -> str:
    sedtlpconfigfile = "w" + settings.tlpconfigfile
    sedcommand = ["sed", "-n", sedtlpconfigfile, tmpconfigfile]

    # check permission and apply sudo if needed
    if not access(settings.tlpconfigfile, W_OK):
        sudo_cmd = get_graphical_sudo()
        if sudo_cmd is None:
            return SUDO_MISSING_TEXT
        sedcommand.insert(0, sudo_cmd)

    check_output(sedcommand)
    return ''
