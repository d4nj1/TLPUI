"""Select UI widget."""

from gi.repository import Gtk
from .. import settings


def create_selection_box(configname: str, values: str) -> Gtk.ComboBox:
    """Create select box."""
    combobox = Gtk.ComboBoxText()
    selectitems = values.split(',')
    configvalue = settings.tlpconfig[configname].get_value()

    if configvalue not in selectitems:
        settings.tlpconfig[configname].stateimage.warn_unknown_config_value(configvalue)

    countid = 0
    selectid = 0

    for item in selectitems:
        combobox.append_text(item)
        if item == configvalue:
            selectid = countid
        countid += 1

    combobox.set_active(selectid)
    combobox.connect('changed', change_selection_state, configname)
    return combobox


def change_selection_state(self: Gtk.ComboBoxText, configname: str):
    """Process and store state change."""
    newvalue = self.get_active_text()
    settings.tlpconfig[configname].set_value(newvalue)
