import configparser
from os import path
from pathlib import Path

# application folder settings
workdir = path.dirname(path.abspath(__file__))
langdir = workdir + '/lang/'
icondir = workdir + '/icons/'

# default user params
language = 'en_EN'
tlpconfigfile = '/etc/default/tlp'
activecategorie = 0
windowxsize = 900
windowysize = 600

# user config
userconfigpath = Path(str(Path.home()) + "/.config/tlpui")
userconfigfile = Path(str(userconfigpath) + "/tlpui.cfg")


def persist():
    config = configparser.ConfigParser()
    config.read_file(open(str(userconfigfile)))
    config['default']['language'] = language
    config['default']['tlpconfigfile'] = tlpconfigfile
    config['default']['activecategorie'] = str(activecategorie)
    config['default']['windowxsize'] = str(windowxsize)
    config['default']['windowysize'] = str(windowysize)
    with open(str(userconfigfile), 'w') as configfile:
        config.write(configfile)


if userconfigfile.exists():
    config = configparser.ConfigParser()
    config.read_file(open(str(userconfigfile)))
    tlpconfigfile = config['default']['tlpconfigfile']
    language = config['default']['language']
    activecategorie = int(config['default']['activecategorie'])
    windowxsize = int(config['default']['windowxsize'])
    windowysize = int(config['default']['windowysize'])
else:
    userconfigpath.mkdir(parents=True, exist_ok=True)
    userconfigfile.touch()
    userconfigfile.write_text("[default]")
    persist()


# runtime params
tlpconfig = dict()
tlpconfig_original = dict()
