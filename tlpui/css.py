"""Provide CSS support for UI."""

from gi.repository import Gtk
from . import settings


def get_css_provider() -> Gtk.CssProvider:
    """Create css provider from stylesheet file and return it."""
    with open(f'{settings.workdir}/styles.css', encoding='utf-8') as cssfile:
        cssdata = cssfile.read()

    cssprovider = Gtk.CssProvider()
    cssprovider.load_from_data(cssdata)

    return cssprovider
