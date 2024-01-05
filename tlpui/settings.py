"""Provide runtime application settings."""

from os import path, getenv
from pathlib import Path
from . import settingshelper

# application folder settings
workdir = path.dirname(path.abspath(__file__))
langdir = f'{workdir}/lang/'
icondir = f'{workdir}/icons/'

# flatpak related params
IS_FLATPAK = Path("/.flatpak-info").exists()
FOLDER_PREFIX = "/var/run/host" if IS_FLATPAK else ""
TMP_FOLDER = f"{getenv('XDG_RUNTIME_DIR')}/app/{getenv('FLATPAK_ID')}" if IS_FLATPAK else None

# check for required commands to exist
settingshelper.check_binaries_exist(FOLDER_PREFIX)

# user config
userconfig = settingshelper.UserConfig()

# runtime params
tlpversion = settingshelper.get_installed_tlp_version()
tlpbaseversion = tlpversion.replace(".", "_")[0:3]
tlpbaseconfigfile = settingshelper.get_tlp_config_file("")
tlpconfigfile = settingshelper.get_tlp_config_file(FOLDER_PREFIX)
tlpconfig = {}
tlpconfig_original = {}
tlpconfig_defaults = {}
active_scroll = None
