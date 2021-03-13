from gi.repository import Gtk
from .. import settings


def create_numeric_spinbutton(configname: str, values: str) -> Gtk.SpinButton:
    valuerange = values.split('-')
    configvalue = settings.tlpconfig[configname].get_value()
    adjustment = Gtk.Adjustment(0, float(valuerange[0]), float(valuerange[1]), 1, 10, 0)

    spinbutton = Gtk.SpinButton()
    spinbutton.set_numeric(True)
    spinbutton.set_adjustment(adjustment)
    spinbutton.set_value(float(configvalue))
    spinbutton.connect('value-changed', change_numeric_spin_value, configname)
    return spinbutton


def change_numeric_spin_value(self: Gtk.SpinButton, configname: str):
    newvalue = str(int(self.get_value()))
    settings.tlpconfig[configname].set_value(newvalue)
