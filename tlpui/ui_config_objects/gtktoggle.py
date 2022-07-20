"""Toggle config state."""

from gi.repository import Gtk
from .. import mainui
from .. import settings


def create_toggle_button(configname: str, configwidget: Gtk.Widget, window: Gtk.Window) -> Gtk.CheckButton:
    """Create state toggle."""
    togglebutton = Gtk.CheckButton()

    if settings.tlpconfig[configname].is_enabled():
        togglebutton.set_active(True)
    else:
        configwidget.set_sensitive(False)

    togglebutton.connect('toggled', on_button_toggled, configname, configwidget, window)
    return togglebutton


def on_button_toggled(self: Gtk.CheckButton, configname: str, configwidget: Gtk.Widget, window: Gtk.Window):
    """Process and store config state."""
    tlpobject = settings.tlpconfig[configname]

    if self.get_active():
        tlpobject.set_enabled(True)
        configwidget.set_sensitive(True)

        # Reset to default when intrinsic default gets reactivated
        if tlpobject.get_value() == "" and settings.tlpconfig_defaults[configname].is_enabled():
            tlpobject.set_value(settings.tlpconfig_defaults[configname].get_value())
            mainui.load_tlp_config(self, window, False)
    else:
        tlpobject.set_enabled(False)
        configwidget.set_sensitive(False)

        # If intrinsic default gets deactivated we have to remove value
        if settings.tlpconfig_defaults[configname].is_enabled():
            tlpobject.set_value("")
