"""Multiselect UI widget."""

from gi.repository import Gtk
from .. import settings


def create_multi_selection_box(configname: str, values: str) -> Gtk.ComboBox:
    """Create multi select box."""
    multiselectbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    multiselectitems = values.split(',')
    configitems = settings.tlpconfig[configname].get_value().split(' ')

    for selectitem in multiselectitems:
        toggle = Gtk.ToggleButton(selectitem)
        if selectitem in configitems:
            toggle.set_active(True)
        toggle.connect('toggled', change_selection_state, configname, multiselectitems)

        multiselectbox.pack_start(toggle, False, False, 2)

    return multiselectbox


def change_selection_state(self: Gtk.ToggleButton, configname: str, checkitems: []):
    """Process and store state change."""
    currentitem = self.get_label()
    currentstate = self.get_active()
    currentvalue = str(settings.tlpconfig[configname].get_value())

    newvalue = ''
    for checkitem in checkitems:
        if checkitem == currentitem and currentstate is False:
            continue
        elif checkitem in currentvalue or checkitem == currentitem:
            newvalue = newvalue + " " + checkitem

    settings.tlpconfig[configname].set_value(newvalue.lstrip())
