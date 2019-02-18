"""This module provides helper functions for TLPUI"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from shutil import which
from . import language


EXPECTED_ITEM_MISSING_TEXT = language.UH_('Expected item missing in config file')  # type: str
SUDO_MISSING_TEXT = language.UH_('Install pkexec, gksu, gksudo, kdesu or kdesudo first.')  # type: str
DEFAULT_STATE_TEXT = language.UH_('Default state:')  # type: str
DEFAULT_VALUE_TEXT = language.UH_('Default value:')  # type: str
CHANGED_STATE_TEXT = language.UH_('CHANGED')  # type: str


def get_graphical_sudo() -> str:
    """Fetch available graphical sudo command"""
    sudo = which("pkexec")
    if sudo is None:
        sudo = which("gksu")
    if sudo is None:
        sudo = which("gksudo")
    if sudo is None:
        sudo = which("kdesu")
    if sudo is None:
        sudo = which("kdesudo")
    return sudo


class StateImage:
    """Class to display configuration item state"""
    def __init__(self, defaultvalue, defaultstate, stateimage: Gtk.Image):
        self.defaultvalue = str(defaultvalue)
        self.defaultstate = bool(defaultstate)
        self.stateimage = stateimage

    def refresh_image_state(self, value: str, store: str, enabled: bool, enabledstore: bool) -> None:
        """Refresh image and description by changed state"""
        changed = False
        if enabled != enabledstore or value != store:
            changed = True

        enabledtext = ''
        if enabled != self.defaultstate:
            enabledtext += '{} {}'.format(DEFAULT_STATE_TEXT, str(self.defaultstate))

        if value == self.defaultvalue:
            if not changed and enabledtext == '':
                self.stateimage.clear()
            elif not changed and enabledtext != '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_INFO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('{}'.format(enabledtext))
            elif changed and enabledtext == '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_UNDO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('{}'.format(CHANGED_STATE_TEXT))
            elif changed and enabledtext != '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_UNDO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('{}\n{}'.format(CHANGED_STATE_TEXT, enabledtext))
        else:
            defaulttext = '{} {}'.format(DEFAULT_VALUE_TEXT, self.defaultvalue)
            if not changed and enabledtext == '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_INFO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text(defaulttext)
            elif not changed and enabledtext != '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_INFO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('{}\n{}'.format(enabledtext, defaulttext))
            elif changed and enabledtext == '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_UNDO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('{}\n{}'.format(CHANGED_STATE_TEXT, defaulttext))
            elif changed and enabledtext != '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_UNDO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('{}\n{}\n{}'.format(CHANGED_STATE_TEXT, enabledtext, defaulttext))
