from gi.repository import Gtk

opacitylevel = 0.3

def create_toggle_button(tlpobject, tlpconfigbox) -> Gtk.CheckButton:
    togglebutton = Gtk.CheckButton()

    if tlpobject.get_state() == True:
        togglebutton.set_active(True)
    else:
        togglebutton.set_active(False)
        tlpconfigbox.set_opacity(opacitylevel)

    togglebutton.connect('toggled', on_button_toggled, tlpobject, tlpconfigbox)
    return togglebutton


def on_button_toggled(self, tlpobject, tlpconfigbox):

    if self.get_active() == True:
        tlpobject.set_new_state(True)
        tlpconfigbox.set_opacity(1)
    else:
        tlpobject.set_new_state(False)
        tlpconfigbox.set_opacity(opacitylevel)

    #print(tlpobject.get_state())
    #print(tlpobject.get_new_state())