"""Switch widget."""

from gi.repository import Gtk
from .. import settings


def create_state_switch(configname: str, values: str) -> Gtk.Switch:
    """Create switch."""
    switch = Gtk.Switch()

    toggleitems = values.split(',')
    falseitem = toggleitems[0]
    trueitem = toggleitems[1]

    if settings.tlpconfig[configname].get_value() == trueitem:
        switch.set_active(True)
    else:
        switch.set_active(False)

    switch.connect('notify::active', change_switch_state, configname, falseitem, trueitem)
    return switch


def change_switch_state(self: Gtk.Switch, notify, configname: str, falseitem: str, trueitem: str):
    """Process and store state change."""
    tlpobject = settings.tlpconfig[configname]

    if self.get_active():
        tlpobject.set_value(trueitem)
    else:
        tlpobject.set_value(falseitem)
