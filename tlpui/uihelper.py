"""This module provides general helper functions for the UI."""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from shutil import which
from pathlib import Path
from . import language
from . import settings
from . import constants
from . import errorui


EXPECTED_ITEM_MISSING_TEXT = language.UH_('Expected item missing in config file')  # type: str
UNKNOWN_CONFIG_VALUE_TEXT = language.UH_('Unknown config value detected')  # type: str
SUDO_MISSING_TEXT = language.UH_('Install pkexec, gksu, gksudo, kdesu or kdesudo first')  # type: str
DEFAULT_STATE_TEXT = language.UH_('Default state:')  # type: str
DEFAULT_VALUE_TEXT = language.UH_('Default value:')  # type: str
CHANGED_STATE_TEXT = language.UH_('CHANGED')  # type: str


def get_graphical_sudo() -> str:
    """Fetch available graphical sudo command."""
    sudo_list = ["pkexec", "gksu", "gksudo", "kdesu", "kdesudo"]
    for sudo in sudo_list:
        if settings.IS_FLATPAK:
            sudo_exists = Path(f"{settings.FOLDER_PREFIX}/usr/bin/{sudo}").exists()
        else:
            sudo_exists = which(sudo) is not None

        if sudo_exists:
            return sudo
    errorui.show_dialog(SUDO_MISSING_TEXT)
    return None


def get_flag_image(locale: str) -> Gtk.Image:
    """Fetch flag image from icons folder."""
    flagpixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(f"{settings.icondir}flags/{locale}.png", width=16, height=16)
    return Gtk.Image().new_from_pixbuf(flagpixbuf)


def get_theme_image(iconname: str, iconsize: Gtk.IconSize) -> Gtk.Image:
    """Fetch image from theme or return fallback if missing."""
    if Gtk.IconTheme.get_default().has_icon(iconname):
        return Gtk.Image().new_from_icon_name(iconname, iconsize)
    return Gtk.Image().new_from_file(f"{settings.icondir}themeable/hicolor/scalable/actions/{iconname}.svg")


class StateImage:
    """Class to display configuration item state."""

    def __init__(self, defaultvalue, defaultstate, stateimage: Gtk.Image):
        """Init state image class parameters."""
        self.defaultvalue = str(defaultvalue)
        self.defaultstate = bool(defaultstate)
        self.stateimage = stateimage

    def warn_unknown_config_value(self, configvalue: str) -> None:
        """Add image and tooltip for unknown values."""
        self.stateimage.set_from_icon_name(constants.ICON_NAME_WARNING, Gtk.IconSize.BUTTON)
        self.stateimage.set_tooltip_text(f'{UNKNOWN_CONFIG_VALUE_TEXT}: {configvalue}')

    def refresh(self, value: str, store: str, enabled: bool, enabledstore: bool) -> None:
        """Refresh image and description by changed state."""
        changed = False
        if enabled != enabledstore or value != store:
            changed = True

        enabledtext = ''
        if enabled != self.defaultstate:
            enabledtext += f'{DEFAULT_STATE_TEXT} {str(self.defaultstate)}'

        if value == self.defaultvalue:
            if not changed and enabledtext == '':
                self.stateimage.clear()
            elif not changed and enabledtext != '':
                self.stateimage.set_from_icon_name(constants.ICON_NAME_INFO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text(f'{enabledtext}')
            elif changed and enabledtext == '':
                self.stateimage.set_from_icon_name(constants.ICON_NAME_UNDO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text(f'{CHANGED_STATE_TEXT}')
            elif changed and enabledtext != '':
                self.stateimage.set_from_icon_name(constants.ICON_NAME_UNDO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text(f'{CHANGED_STATE_TEXT}\n{enabledtext}')
        else:
            defaulttext = f'{DEFAULT_VALUE_TEXT} {self.defaultvalue}'
            if not changed and enabledtext == '':
                self.stateimage.set_from_icon_name(constants.ICON_NAME_INFO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text(defaulttext)
            elif not changed and enabledtext != '':
                self.stateimage.set_from_icon_name(constants.ICON_NAME_INFO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text(f'{enabledtext}\n{defaulttext}')
            elif changed and enabledtext == '':
                self.stateimage.set_from_icon_name(constants.ICON_NAME_UNDO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text(f'{CHANGED_STATE_TEXT}\n{defaulttext}')
            elif changed and enabledtext != '':
                self.stateimage.set_from_icon_name(constants.ICON_NAME_UNDO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text(f'{CHANGED_STATE_TEXT}\n{enabledtext}\n{defaulttext}')
