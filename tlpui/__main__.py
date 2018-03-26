#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from pathlib import Path
import copy

from . import settings
from .css import get_css_provider
from .file import read_tlp_file_config
from .mainui import create_main_box, store_windowsize, window_key_events, close_main_window, tlp_file_chooser

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    get_css_provider(),
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


def main() -> None:
    window = Gtk.Window()

    if not Path(settings.tlpconfigfile).exists():
        tlp_file_chooser(window)

    settings.tlpconfig = read_tlp_file_config(settings.tlpconfigfile)
    settings.tlpconfig_original = copy.deepcopy(settings.tlpconfig)

    window.set_title('TLP-UI')
    window.set_default_size(settings.windowxsize, settings.windowysize)
    window.add(create_main_box(window))
    window.connect('check-resize', store_windowsize)
    window.connect('delete-event', close_main_window)
    window.connect('key-press-event', window_key_events)
    window.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
