import sys
from gi.repository import Gtk
from shutil import which
from subprocess import check_output, STDOUT
from . import language
from .uihelper import get_theme_image, get_graphical_sudo, SUDO_MISSING_TEXT


TLP_STAT_MISSING = language.ST_('tlp-stat executable not found.')  # type: str


def fetch_simple_stats(_, textbuffer: Gtk.TextBuffer) -> None:
    tlp_stat_cmd = which("tlp-stat")

    if tlp_stat_cmd is None:
        textbuffer.set_text(TLP_STAT_MISSING)
        return

    simple_stat_command = ["tlp-stat", "-r", "-t", "-c", "-s", "-u"]
    tlp_stat_output = call_tlp_stat(simple_stat_command)
    textbuffer.set_text(tlp_stat_output)


def fetch_complete_stats(_, textbuffer: Gtk.TextBuffer) -> None:
    sudo_cmd = get_graphical_sudo()
    tlp_stat_cmd = which("tlp-stat")

    if sudo_cmd is None:
        textbuffer.set_text(SUDO_MISSING_TEXT)
        return

    if tlp_stat_cmd is None:
        textbuffer.set_text(TLP_STAT_MISSING)
        return

    tlp_stat_output = call_tlp_stat([sudo_cmd, "tlp-stat"])
    textbuffer.set_text(tlp_stat_output)


def call_tlp_stat(command) -> str:
    return check_output(command, stderr=STDOUT).decode(sys.stdout.encoding)


def create_stat_box() -> Gtk.Box:
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

    fetchsimplebutton = Gtk.Button(label=' {}'.format(language.ST_('Simple')), image=get_theme_image('dialog-information-symbolic', Gtk.IconSize.BUTTON))
    fetchsimplebutton.connect('clicked', fetch_simple_stats, textbuffer)
    fetchsimplebutton.set_always_show_image(True)

    fetchcompletebutton = Gtk.Button(label=' {}'.format(language.ST_('Complete')), image=get_theme_image('format-indent-more-symbolic', Gtk.IconSize.BUTTON))
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
