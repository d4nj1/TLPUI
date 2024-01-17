"""This module provides helper functions for application settings."""

import configparser
import re
import sys
from os import getenv
from shutil import which
from subprocess import check_output, CalledProcessError
from pathlib import Path
from . import errorui


def exec_command(commands: [str]):
    """Execute commands locally."""
    try:
        return check_output(commands).decode(sys.stdout.encoding)
    except CalledProcessError as error:
        errorui.show_dialog(error)


def get_tlp_config_file(prefix: str) -> str:
    """Select tlp config file by prefix."""
    return f"{prefix}/etc/tlp.conf"


def check_binaries_exist(flatpak_folder_prefix: str) -> None:
    """Check if required binaries are installed on system."""
    for expected_command in ["tlp", "tlp-stat", "lspci", "lsusb"]:
        if flatpak_folder_prefix != "":
            command_exists = Path(f"{flatpak_folder_prefix}/usr/bin/{expected_command}").exists()
            if not command_exists:
                command_exists = Path(f"{flatpak_folder_prefix}/usr/sbin/{expected_command}").exists()
        else:
            command_exists = which(expected_command) is not None
            if not command_exists:
                command_exists = Path(f"/usr/sbin/{expected_command}").exists()

        if not command_exists:
            errorui.show_dialog(f"{expected_command} not found on system. Please install first.")
            sys.exit(1)


def get_installed_tlp_version() -> str:
    """Fetch tlp version from command."""
    pattern = re.compile(r"TLP ([^\s]+)")
    currentconfig = exec_command(["tlp-stat", "-c"])
    matcher = pattern.search(currentconfig)
    return matcher.group(1)


def get_user_config_file() -> Path:
    """Get config path for executing user."""
    userconfighome = getenv("XDG_CONFIG_HOME", "")
    if userconfighome == "":
        userconfigpath = Path(str(Path.home()) + "/.config/tlpui")
    else:
        userconfigpath = Path(str(userconfighome) + "/tlpui")
    return Path(str(userconfigpath) + "/tlpui.cfg")


class UserConfig:
    """Class to handle ui config parameters."""

    def __init__(self):
        """Init user config class parameters."""
        self.language = "en_EN"
        self.activeoption = 0
        self.activecategory = 0
        self.activeposition = 0
        self.windowxsize = 900
        self.windowysize = 600
        self.userconfigfile = get_user_config_file()
        self.read_user_config()

    def read_user_config(self):
        """Read ui config parameters from user home."""
        if self.userconfigfile.exists():
            config = configparser.ConfigParser()
            with open(str(self.userconfigfile), encoding='utf-8') as configfile:
                config.read_file(configfile)
            try:
                self.language = config['default']['language']
                self.activeoption = int(config['default']['activeoption'])
                self.activecategory = int(config['default']['activecategory'])
                self.activeposition = float(config['default']['activeposition'])
                self.windowxsize = int(config['default']['windowxsize'])
                self.windowysize = int(config['default']['windowysize'])
            except KeyError:
                # Config key error, override with default values
                self.write_user_config()
        else:
            self.userconfigfile.parent.mkdir(parents=True, exist_ok=True)
            self.write_user_config()

    def write_user_config(self):
        """Persist ui config parameters to user home."""
        config = configparser.ConfigParser()
        config['default'] = {}
        config['default']['language'] = self.language
        config['default']['activeoption'] = str(self.activeoption)
        config['default']['activecategory'] = str(self.activecategory)
        config['default']['activeposition'] = str(self.activeposition)
        config['default']['windowxsize'] = str(self.windowxsize)
        config['default']['windowysize'] = str(self.windowysize)
        with open(str(self.userconfigfile), mode='w', encoding='utf-8') as configfile:
            config.write(configfile)
