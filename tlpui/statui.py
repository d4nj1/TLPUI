"""This module provides general tlp-stat functions for the UI."""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from . import language
from . import settingshelper
from .uihelper import get_theme_image, get_graphical_sudo


def fetch_simple_stats(_, textbuffer: Gtk.TextBuffer) -> None:
    """Fetch simple tlp-stat information."""
    simple_stat_command = ["tlp-stat", "-r", "-t", "-c", "-s", "-u"]
    tlp_stat_output = settingshelper.exec_command(simple_stat_command)
    textbuffer.set_text(tlp_stat_output)


def fetch_complete_stats(_, textbuffer: Gtk.TextBuffer) -> None:
    """Fetch complete tlp-stat information."""
    sudo_cmd = get_graphical_sudo()

    if sudo_cmd is None:
        return

    tlp_stat_output = settingshelper.exec_command([sudo_cmd, "tlp-stat"])
    textbuffer.set_text(tlp_stat_output)


def create_stat_box() -> Gtk.Box:
    """Create box with stat widgets."""
    scrolledwindow = Gtk.ScrolledWindow()
    scrolledwindow.set_hexpand(True)
    scrolledwindow.set_vexpand(True)

    textbuffer = Gtk.TextBuffer()
    textbuffer.set_text(language.ST_('Click fetch button to receive results'))

    textview = Gtk.TextView()
    textview.set_buffer(textbuffer)
    textview.set_editable(False)

    scrolledwindow.add(textview)

    emptylabel = Gtk.Label()

    fetchsimplebutton = Gtk.Button(label=f" {language.ST_('Simple')}",
                                   image=get_theme_image('dialog-information-symbolic', Gtk.IconSize.BUTTON))
    fetchsimplebutton.connect('clicked', fetch_simple_stats, textbuffer)
    fetchsimplebutton.set_always_show_image(True)

    fetchcompletebutton = Gtk.Button(label=f" {language.ST_('Complete')}",
                                     image=get_theme_image('format-indent-more-symbolic', Gtk.IconSize.BUTTON))
    fetchcompletebutton.connect('clicked', fetch_complete_stats, textbuffer)
    fetchcompletebutton.set_always_show_image(True)

    buttonbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    buttonbox.pack_start(emptylabel, True, True, 0)
    buttonbox.pack_start(fetchsimplebutton, False, False, 0)
    buttonbox.pack_start(fetchcompletebutton, False, False, 0)

    statbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    statbox.set_margin_top(18)
    statbox.set_margin_bottom(18)
    statbox.set_margin_left(18)
    statbox.set_margin_right(18)
    statbox.pack_start(buttonbox, False, False, 0)
    statbox.pack_start(scrolledwindow, True, True, 0)

    return statbox
