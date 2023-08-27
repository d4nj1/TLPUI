"""This module provides error helper functions for the UI."""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def show_dialog(error_message) -> None:
    """Show error dialog."""
    dialog = Gtk.MessageDialog()
    dialog.set_default_size(150, 100)
    dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
    dialog.format_secondary_markup(error_message)
    dialog.run()
    dialog.destroy()
