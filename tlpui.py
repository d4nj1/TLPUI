from gi.repository import Gtk, Gdk

from css import get_css_provider
from file import read_tlp_file_config
from mainui import create_main_box, close_window

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    get_css_provider(),
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

defaultconfigpath = '/etc/default/tlp'
tlpconfig = read_tlp_file_config(defaultconfigpath)

window = Gtk.Window()
window.set_default_size(900, 600)
window.add(create_main_box(window, defaultconfigpath, tlpconfig))
window.connect('delete-event', Gtk.main_quit)
window.connect('key-press-event', close_window)
window.show_all()
Gtk.main()
