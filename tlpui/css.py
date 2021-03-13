"""Provide CSS support for UI."""

from gi.repository import Gtk
from . import settings


def get_css_provider() -> Gtk.CssProvider:
    """Create css provider from stylesheet file and return it."""
    cssfile = open(settings.workdir + '/styles.css', 'rb')
    cssdata = cssfile.read()
    cssfile.close()

    cssprovider = Gtk.CssProvider()
    cssprovider.load_from_data(cssdata)

    return cssprovider
