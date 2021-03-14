"""Disk view UI widget."""

from gi.repository import Gtk
from .. import settings


def create_view(configname: str) -> Gtk.Box:
    """Create disk view."""
    tlpobject = settings.tlpconfig[configname]
    label = Gtk.Label(tlpobject.get_value())
    label.set_width_chars(len(tlpobject.get_value()) + 5)
    return label
