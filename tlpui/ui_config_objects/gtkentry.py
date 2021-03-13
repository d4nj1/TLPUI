from gi.repository import Gtk
from .. import settings


def create_entry(configname: str) -> Gtk.Entry:
    configvalue = settings.tlpconfig[configname].get_value()
    configvaluelength = len(configvalue)
    if configvaluelength >= 70:
        configvaluelength = 70

    entry = Gtk.Entry()
    entry.set_text(configvalue)
    entry.set_width_chars(configvaluelength + 5)
    entry.connect('changed', change_entry_text, configname)
    return entry


def change_entry_text(self: Gtk.Entry, configname: str):
    settings.tlpconfig[configname].set_value(self.get_text())
