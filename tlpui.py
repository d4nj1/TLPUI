import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from os import path
from css import get_css_provider
from file import read_tlp_file_config
from mainui import create_main_box, close_window

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    get_css_provider(),
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

defaultconfigpath = '/etc/default/tlp'

window = Gtk.Window()
window.set_title('TLP-UI')
window.set_default_size(900, 600)

if path.exists(defaultconfigpath):
    tlpconfig = read_tlp_file_config(defaultconfigpath)
    window.add(create_main_box(window, defaultconfigpath, tlpconfig))
else:
    noconfiglabel = Gtk.Label("No config file found at " + defaultconfigpath)
    noconfigbox = Gtk.Box()
    noconfigbox.pack_start(noconfiglabel, True, True, 0)
    window.add(noconfigbox)

window.connect('delete-event', Gtk.main_quit)
window.connect('key-press-event', close_window)
window.show_all()
Gtk.main()
