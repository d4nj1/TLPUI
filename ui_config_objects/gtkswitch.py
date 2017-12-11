from gi.repository import Gtk

def create_state_switch(values, tlpobject) -> Gtk.Switch:
    switch = Gtk.Switch()

    toggleitems = values.split(',')
    falseitem = toggleitems[0]
    trueitem = toggleitems[1]

    if tlpobject.get_value() == trueitem:
        switch.set_active(True)
    else:
        switch.set_active(False)

    switch.connect('notify::active', change_switch_state, tlpobject, falseitem, trueitem)
    return switch

def change_switch_state(self, notify, tlpobject, falseitem, trueitem):

    if self.get_active():
        tlpobject.set_value(trueitem)
    else:
        tlpobject.set_value(falseitem)
