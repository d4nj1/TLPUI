from gi.repository import Gtk


def create_view(tlpobject) -> Gtk.Box:
    label = Gtk.Label(tlpobject.get_value())
    label.set_width_chars(len(tlpobject.get_value())+5)

    return label
