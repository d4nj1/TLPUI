from gi.repository import Gtk
import settings

def get_css_provider() -> Gtk.CssProvider:
    cssfile = open(settings.workdir + '/styles.css', 'rb')
    cssdata = cssfile.read()
    cssfile.close()

    cssprovider = Gtk.CssProvider()
    cssprovider.load_from_data(cssdata)

    return cssprovider