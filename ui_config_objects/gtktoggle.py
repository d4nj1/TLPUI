from gi.repository import Gtk

opacitylevel = 0.3

def create_toggle_button(tlpobject, tlpconfigbox) -> Gtk.ToggleButton:
    togglebutton = Gtk.ToggleButton()

    if tlpobject.get_state() == True:
        togglebutton.set_active(True)
        togglebutton.set_image(Gtk.Image(stock=Gtk.STOCK_YES))
    else:
        togglebutton.set_active(False)
        togglebutton.set_image(Gtk.Image(stock=Gtk.STOCK_NO))
        tlpconfigbox.set_opacity(opacitylevel)

    togglebutton.connect('toggled', on_button_toggled, tlpobject, tlpconfigbox)
    return togglebutton


def on_button_toggled(self, tlpobject, tlpconfigbox):

    if self.get_active() == True:
        self.set_image(Gtk.Image(stock=Gtk.STOCK_YES))
        tlpobject.set_new_state(True)
        tlpconfigbox.set_opacity(1)
    else:
        self.set_image(Gtk.Image(stock=Gtk.STOCK_NO))
        tlpobject.set_new_state(False)
        tlpconfigbox.set_opacity(opacitylevel)

    #print(tlpobject.get_state())
    #print(tlpobject.get_new_state())