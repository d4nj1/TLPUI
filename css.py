from gi.repository import Gtk
from os import path

cwd = path.dirname(path.abspath(__file__)) + '/'

def get_css_provider() -> Gtk.CssProvider:
    cssfile = open(cwd + 'styles.css', 'rb')
    cssdata = cssfile.read()
    cssfile.close()

    cssprovider = Gtk.CssProvider()
    cssprovider.load_from_data(cssdata)

    return cssprovider