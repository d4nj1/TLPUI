from gi.repository import Gtk

def create_selection_box(values, tlpobject) -> Gtk.ComboBox:
    combobox = Gtk.ComboBoxText()
    selectitems = values.split(',')
    configvalue = tlpobject.get_value()

    countid = 0
    selectid = 0

    for item in selectitems:
        combobox.append_text(item)
        if item in configvalue:
            selectid = countid
        countid += 1

    combobox.set_active(selectid)
    combobox.connect('changed', change_selection_state, tlpobject)
    return combobox


def change_selection_state(self, tlpobject):
    newvalue = self.get_active_text()
    # print(newvalue)
    tlpobject.set_value(newvalue)