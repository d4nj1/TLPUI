from gi.repository import Gtk


def create_multi_selection_box(values, tlpobject) -> Gtk.ComboBox:
    multiselectbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    multiselectitems = values.split(',')
    configitems = tlpobject.get_value().split(' ')

    toggles = []

    for item in multiselectitems:
        toggle = Gtk.ToggleButton(item)
        if item in configitems:
            toggle.set_active(True)
        toggles.append(toggle)
        multiselectbox.pack_start(toggle, False, False, 2)

    for toggle in toggles:
        toggle.connect('toggled', change_selection_state, toggles, tlpobject)

    return multiselectbox


def change_selection_state(self, toggles, tlpobject):
    newvalue = ""
    for toggle in toggles:
        if toggle.get_active():
            newvalue += " " + toggle.get_label()

    tlpobject.set_value(newvalue.lstrip())
