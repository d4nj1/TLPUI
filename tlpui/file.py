"""Provide file handling."""

import copy
import re
from io import open
from os import access, W_OK, close, path
from tempfile import mkstemp
from .config import TlpConfig, ConfType
from . import settings
from . import settingshelper
from .filehelper import get_yaml_schema_object_from_file, extract_default_tlp_configs, TlpDefaults
from .uihelper import get_graphical_sudo


def get_yaml_schema_object(objectname) -> dict:
    """Get Json schema for installed TLP version."""
    tlpprovidedschema = '/usr/share/tlp-pm/configschema.yaml'
    if path.exists(tlpprovidedschema):
        return get_yaml_schema_object_from_file(objectname, tlpprovidedschema)
    majorminor = settings.tlpbaseversion
    return get_yaml_schema_object_from_file(objectname, f"{settings.workdir}/configschema/{majorminor}.yaml")


def get_tlp_config_defaults(tlpversion: str):
    """Fetch TLP default configs."""
    tlpconfig_defaults = extract_default_tlp_configs(f"{settings.workdir}/defaults/tlp-{tlpversion}.conf")

    # update default values with intrinsic ones
    intrinsic_defaults_path = f"{settings.FOLDER_PREFIX}/usr/share/tlp/defaults.conf"
    tlpconfig_defaults.update(extract_default_tlp_configs(intrinsic_defaults_path))

    return tlpconfig_defaults


def init_tlp_file_config() -> None:
    """Load current TLP config settings."""
    settings.tlpconfig = {}
    tlpversion = settings.tlpbaseversion
    settings.tlpconfig_defaults = get_tlp_config_defaults(tlpversion)

    # get current settings from tlp itself
    tlpstat = settingshelper.exec_command(["tlp-stat", "-c"])
    tlpsettinglines = tlpstat.split('\n')

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


def extract_tlp_settings(lines: list) -> None:
    """Extract TLP config locations and values."""
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
                print(f'Config type not found for file: {configfile}')
                conftype = ConfType.ERR

            configproperty = settingsparts[2].split('=', maxsplit=1)
            configname = configproperty[0]
            configvalue = configproperty[1]

            if configvalue.startswith('\"') and configvalue.endswith('\"'):
                configvalue = configvalue.lstrip('\"').rstrip('\"')

            enabled = configvalue != ""

            settings.tlpconfig[configname] = TlpConfig(enabled, configname, configvalue, conftype, configfile)


def get_changed_properties() -> dict:
    """Evaluate changed settings from UI."""
    changedproperties = {}

    changed = settings.tlpconfig
    original = settings.tlpconfig_original

    for configid in changed:
        config = changed[configid]              # type: TlpConfig
        config_original = original[configid]    # type: TlpConfig

        statechange = config.is_enabled() != config_original.is_enabled()
        configchange = config.get_value() != config_original.get_value()

        if statechange or configchange:
            configname = config.get_name()
            value = config.get_value()

            if not config.is_enabled() and settings.tlpconfig_defaults[configname].is_enabled():
                enabled = ""
            else:
                enabled = "" if config.is_enabled() else "#"

            if settings.tlpconfig_defaults[configname].is_quoted():
                value = f"\"{value}\""

            changedproperties[configname] = f"{enabled}{configname}={value}"

    return changedproperties


def create_tmp_tlp_config_file(changedproperties: dict) -> str:
    """Create tmp file to prepare writing new config."""
    propertypattern = re.compile(r'^#?[A-Z_\d]+=')
    filehandler, tmpfilename = mkstemp(dir=settings.TMP_FOLDER)
    newfile = open(tmpfilename, mode='w', encoding='utf-8')

    oldfile = open(settings.tlpconfigfile, encoding='utf-8')
    lines = oldfile.readlines()
    oldfile.close()

    for line in lines:
        if propertypattern.match(line):
            cleanline = line.lstrip().lstrip('#')

            configproperty = cleanline.split('=', maxsplit=1)
            configname = configproperty[0]

            if configname in changedproperties.keys():
                if cleanline.startswith(configname + "="):
                    newfile.write(changedproperties[configname] + '\n')
                    continue

        newfile.write(line)

    newfile.close()
    close(filehandler)
    oldfile.close()

    return tmpfilename


def write_tlp_config(tmpconfigfile: str):
    """Write changes to config file."""
    sedtlpconfigfile = "w" + settings.tlpbaseconfigfile
    sedcommand = ["sed", "-n", sedtlpconfigfile, tmpconfigfile]

    # check permission and apply sudo if needed
    if not access(settings.tlpconfigfile, W_OK):
        sudo_cmd = get_graphical_sudo()
        if sudo_cmd is None:
            return
        sedcommand.insert(0, sudo_cmd)
    settingshelper.exec_command(sedcommand)
