from gi.repository import Gtk

opacitylevel = 0.3

def create_toggle_button(tlpobject, tlpconfigbox) -> Gtk.CheckButton:
    togglebutton = Gtk.CheckButton()

    if tlpobject.is_enabled():
        togglebutton.set_active(True)
    else:
        tlpconfigbox.set_opacity(opacitylevel)

    togglebutton.connect('toggled', on_button_toggled, tlpobject, tlpconfigbox)
    return togglebutton


def on_button_toggled(self, tlpobject, tlpconfigbox):

    if self.get_active():
        tlpobject.set_enabled(True)
        tlpconfigbox.set_opacity(1)
    else:
        tlpobject.set_enabled(False)
        tlpconfigbox.set_opacity(opacitylevel)
