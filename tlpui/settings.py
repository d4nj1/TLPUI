"""This module provides runtime application settings"""

from os import path, getenv
from pathlib import Path
from . import settingshelper

# application folder settings
workdir = path.dirname(path.abspath(__file__))
langdir = workdir + '/lang/'
icondir = workdir + '/icons/'

# user config
userconfig = settingshelper.UserConfig()

# flatpak related params
isflatpak = Path("/.flatpak-info").exists()
folder_prefix = "/var/run/host" if isflatpak else ""
tmpfolder = f"{getenv('XDG_RUNTIME_DIR')}/app/{getenv('FLATPAK_ID')}" if isflatpak else None

# runtime params
tlpbaseversion = settingshelper.get_installed_major_minor_version()
tlpbaseconfigfile = settingshelper.get_tlp_config_file(tlpbaseversion, "")
tlpconfigfile = settingshelper.get_tlp_config_file(tlpbaseversion, folder_prefix)
tlpconfig = dict()
tlpconfig_original = dict()
tlpconfig_defaults = dict()
imagestate = dict()
