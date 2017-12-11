from gi.repository import Gtk

def create_entry(tlpobject) -> Gtk.Entry:
    configvalue = tlpobject.get_value()
    configvaluelength = len(configvalue)
    if configvaluelength >= 70:
        configvaluelength = 70

    entry = Gtk.Entry()
    entry.set_text(configvalue)
    entry.set_width_chars(configvaluelength+5)
    entry.connect('changed', change_entry_text, tlpobject)
    return entry


def change_entry_text(self, tlpobject):
    newvalue = self.get_text()
    # print(newvalue)
    tlpobject.set_value(newvalue)