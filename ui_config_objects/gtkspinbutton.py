from gi.repository import Gtk

def create_numeric_spinbutton(values, tlpobject) -> Gtk.SpinButton:
    range = values.split('-')
    configvalue = tlpobject.get_value()
    adjustment = Gtk.Adjustment(0, float(range[0]), float(range[1]), 1, 10, 0)

    spinbutton = Gtk.SpinButton()
    spinbutton.set_numeric(True)
    spinbutton.set_adjustment(adjustment)
    spinbutton.set_value(float(configvalue))
    spinbutton.connect('value-changed', change_numeric_spin_value, tlpobject)
    return spinbutton


def change_numeric_spin_value(self, tlpobject):
    newvalue = str(int(self.get_value()))
    tlpobject.set_value(newvalue)
