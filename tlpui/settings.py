"""Provide runtime application settings."""

from os import path, getenv
from pathlib import Path
from . import settingshelper

# application folder settings
workdir = path.dirname(path.abspath(__file__))
langdir = f'{workdir}/lang/'
icondir = f'{workdir}/icons/'

# user config
userconfig = settingshelper.UserConfig()

# flatpak related params
IS_FLATPAK = Path("/.flatpak-info").exists()
FOLDER_PREFIX = "/var/run/host" if IS_FLATPAK else ""
TMP_FOLDER = f"{getenv('XDG_RUNTIME_DIR')}/app/{getenv('FLATPAK_ID')}" if IS_FLATPAK else None

# runtime params
tlpbaseversion = settingshelper.get_installed_major_minor_version()
tlpbaseconfigfile = settingshelper.get_tlp_config_file(tlpbaseversion, "")
tlpconfigfile = settingshelper.get_tlp_config_file(tlpbaseversion, FOLDER_PREFIX)
tlpconfig = dict()
tlpconfig_original = dict()
tlpconfig_defaults = dict()
active_scroll = None
