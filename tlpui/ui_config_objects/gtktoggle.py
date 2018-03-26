from gi.repository import Gtk
from .. import settings

opacitylevel = 0.3

def create_toggle_button(configname:str, tlpconfigbox: Gtk.Box) -> Gtk.CheckButton:
    togglebutton = Gtk.CheckButton()

    if settings.tlpconfig[configname].is_enabled():
        togglebutton.set_active(True)
    else:
        tlpconfigbox.set_opacity(opacitylevel)

    togglebutton.connect('toggled', on_button_toggled, configname, tlpconfigbox)
    return togglebutton


def on_button_toggled(self: Gtk.CheckButton, configname: str, tlpconfigbox: Gtk.Box):
    tlpobject = settings.tlpconfig[configname]

    if self.get_active():
        tlpobject.set_enabled(True)
        tlpconfigbox.set_opacity(1)
    else:
        tlpobject.set_enabled(False)
        tlpconfigbox.set_opacity(opacitylevel)
