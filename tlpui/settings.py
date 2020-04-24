import configparser
import re
import sys
from subprocess import check_output
from os import path, getenv
from pathlib import Path

# application folder settings
workdir = path.dirname(path.abspath(__file__))
langdir = workdir + '/lang/'
icondir = workdir + '/icons/'

# default user params
language = 'en_EN'
activeoption = 0
activecategory = 0
windowxsize = 900
windowysize = 600

# user config
userconfighome = getenv("XDG_CONFIG_HOME", "")
if userconfighome == "":
    userconfigpath = Path(str(Path.home()) + "/.config/tlpui")
else:
    userconfigpath = Path(str(userconfighome) + "/tlpui")
userconfigfile = Path(str(userconfigpath) + "/tlpui.cfg")


def persist():
    config = configparser.ConfigParser()
    config['default'] = {}
    config['default']['language'] = language
    config['default']['activeoption'] = str(activeoption)
    config['default']['activecategory'] = str(activecategory)
    config['default']['windowxsize'] = str(windowxsize)
    config['default']['windowysize'] = str(windowysize)
    with open(str(userconfigfile), 'w') as configfile:
        config.write(configfile)


def get_tlp_config_file(version: str) -> str:
    if version in ["0_8", "0_9", "1_0", "1_1", "1_2"]:
        return "/etc/default/tlp"

    return "/etc/tlp.conf"


def get_installed_tlp_version() -> str:
    pattern = re.compile(r"TLP ([^\s]+)")
    currentconfig = check_output(["tlp-stat", "-c"]).decode(sys.stdout.encoding)
    matcher = pattern.search(currentconfig)
    version = matcher.group(1).replace(".", "_")
    return version


def get_installed_major_minor_version() -> str:
    return get_installed_tlp_version()[0:3]


if userconfigfile.exists():
    config = configparser.ConfigParser()
    with open(str(userconfigfile)) as configfile:
        config.read_file(configfile)
    try:
        language = config['default']['language']
        activeoption = int(config['default']['activeoption'])
        activecategory = int(config['default']['activecategory'])
        windowxsize = int(config['default']['windowxsize'])
        windowysize = int(config['default']['windowysize'])
    except KeyError:
        # Config key error, override with default values
        persist()
else:
    userconfigpath.mkdir(parents=True, exist_ok=True)
    persist()


# runtime params
tlpbaseversion = get_installed_major_minor_version()
tlpconfigfile = get_tlp_config_file(tlpbaseversion)
tlpconfig = dict()
tlpconfig_original = dict()
tlpconfig_defaults = dict()
imagestate = dict()
