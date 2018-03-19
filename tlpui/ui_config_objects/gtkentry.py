from gi.repository import Gtk
from ..config import TlpConfig


def create_entry(tlpobject: TlpConfig) -> Gtk.Entry:
    configvalue = tlpobject.get_value()
    configvaluelength = len(configvalue)
    if configvaluelength >= 70:
        configvaluelength = 70

    entry = Gtk.Entry()
    entry.set_text(configvalue)
    entry.set_width_chars(configvaluelength+5)
    entry.connect('changed', change_entry_text, tlpobject)
    return entry


def change_entry_text(self, tlpobject: TlpConfig):
    tlpobject.set_value(self.get_text())
