"""Provide CSS support for UI."""

from gi.repository import Gtk
from . import settings


def get_css_provider() -> Gtk.CssProvider:
    """Create css provider from stylesheet file and return it."""
    cssprovider = Gtk.CssProvider()
    cssprovider.load_from_path(f'{settings.workdir}/styles.css')

    return cssprovider
