"""Checkbutton UI widget."""

from gi.repository import Gtk
from .. import settings


def create_checkbutton_box(configname: str, values: str) -> Gtk.Box:
    """Create checkbutton box."""
    checkbox = Gtk.Box()
    checkitems = values.split(',')
    configvalue = settings.tlpconfig[configname].get_value()

    checkbuttonitem = 0
    for checkitem in checkitems:
        checkbutton = Gtk.CheckButton(checkitem)
        if checkitem in configvalue:
            checkbutton.set_active(True)
        checkbutton.connect('toggled', change_check_state, configname, checkitems)

        if checkbuttonitem % 2 == 0:
            checkbox.pack_start(checkbutton, False, False, 0)
        else:
            checkbox.pack_start(checkbutton, False, False, 12)
        checkbuttonitem += 1

    return checkbox


def change_check_state(self: Gtk.CheckButton, configname: str, checkitems: []):
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
