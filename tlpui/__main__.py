#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

from . import settings
from .css import get_css_provider
from .file import init_tlp_file_config
from .mainui import create_main_box, store_window_size, window_key_events, close_main_window

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    get_css_provider(),
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

# Set window properties
GLib.set_prgname('tlp-ui')
Gdk.set_program_class('Tlp-UI')

# Apply custom scalable icons to icon theme
Gtk.IconTheme().get_default().append_search_path(settings.icondir + 'themeable')

def main() -> None:
    # init configuration settings
    init_tlp_file_config()

    # init application window
    window = Gtk.Window()
    window.set_title('Tlp-UI')
    window.set_icon_name(get_default_icon_name())
    window.set_default_size(settings.windowxsize, settings.windowysize)
    window.add(create_main_box(window))
    window.connect('check-resize', store_window_size)
    window.connect('delete-event', close_main_window)
    window.connect('key-press-event', window_key_events)
    window.show_all()
    Gtk.main()


def get_default_icon_name() -> str:
    if Gtk.IconTheme.get_default().has_icon('preferences-system-power-management'):
        return 'preferences-system-power-management'
    else:
        return 'preferences-system-power'


if __name__ == '__main__':
    main()
