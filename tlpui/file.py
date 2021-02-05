
import copy
import re
from sys import stdout
from subprocess import check_output, STDOUT, CalledProcessError
from io import open
from os import access, W_OK, close, path
from tempfile import mkstemp
from .config import TlpConfig, ConfType
from . import settings
from .filehelper import get_json_schema_object_from_file, extract_default_tlp_configs, TlpDefaults
from .uihelper import get_graphical_sudo, SUDO_MISSING_TEXT


def get_json_schema_object(objectname) -> dict:
    tlpprovidedschema = '/usr/share/tlp-pm/configschema.json'
    if path.exists(tlpprovidedschema):
        return get_json_schema_object_from_file(objectname, tlpprovidedschema)
    else:
        majorminor = settings.tlpbaseversion
        return get_json_schema_object_from_file(objectname, f"{settings.workdir}/configschema/{majorminor}.json")


def get_tlp_config_defaults(tlpversion: str):
    tlpconfig_defaults = extract_default_tlp_configs(f"{settings.workdir}/defaults/tlp-{tlpversion}.conf")

    if tlpversion not in ["0_8", "0_9", "1_0", "1_1", "1_2"]:
        # update default values with intrinsic ones
        intrinsic_defaults_path = f"{settings.folder_prefix}/usr/share/tlp/defaults.conf"
        tlpconfig_defaults.update(extract_default_tlp_configs(intrinsic_defaults_path))

    return tlpconfig_defaults


def init_tlp_file_config() -> None:
    settings.tlpconfig = dict()
    tlpversion = settings.tlpbaseversion
    settings.tlpconfig_defaults = get_tlp_config_defaults(tlpversion)

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


def get_changed_properties() -> dict:
    changedproperties = dict()

    changed = settings.tlpconfig
    original = settings.tlpconfig_original

    for configid in changed:
        config = changed[configid]              # type: TlpConfig
        config_original = original[configid]    # type: TlpConfig

        statechange = config.is_enabled() != config_original.is_enabled()
        configchange = config.get_value() != config_original.get_value()

        if statechange or configchange:
            configname = config.get_name()

            if not config.is_enabled() and settings.tlpconfig_defaults[configname].is_enabled():
                enabled = ""
                value = "* empty"
            else:
                enabled = "" if config.is_enabled() else "#"
                value = config.get_value()

            value = '\"' + value + '\"'
            changedproperties[configname] = "{}{}={}".format(enabled, configname, value)

    return changedproperties


def create_tmp_tlp_config_file(changedproperties: dict) -> str:
    propertypattern = re.compile(r'^#?[A-Z_\d]+=')
    fh, tmpfilename = mkstemp(dir=settings.tmpfolder)
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
    sedtlpconfigfile = "w" + settings.tlpbaseconfigfile
    sedcommand = ["sed", "-n", sedtlpconfigfile, tmpconfigfile]

    # check permission and apply sudo if needed
    if not access(settings.tlpconfigfile, W_OK):
        sudo_cmd = get_graphical_sudo()
        if sudo_cmd is None:
            return SUDO_MISSING_TEXT
        sedcommand.insert(0, sudo_cmd)

    try:
        check_output(sedcommand)
    except CalledProcessError as error:
        print(error)
    return ""
