from gi.repository import Gtk

def get_css_provider() -> Gtk.CssProvider:
    cssfile = open('styles.css', 'rb')
    cssdata = cssfile.read()
    cssfile.close()

    cssprovider = Gtk.CssProvider()
    cssprovider.load_from_data(cssdata)

    return cssprovider