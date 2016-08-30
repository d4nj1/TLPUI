import sys
from gi.repository import Gtk
from shutil import which
from subprocess import check_output


def get_graphical_sudo():
    sudo = which("gksudo")
    if sudo == None:
        sudo = which("kdesudo")
    if sudo == None:
        sudo = which("gksu")
    return sudo


def fetch_tlp_stat(self, textbuffer):
    sudo_cmd = get_graphical_sudo()
    tlpstat_cmd = which("tlp-stat")

    if sudo_cmd == None:
        textbuffer.set_text('Install gksudo, kdesudo or gksu first.')
        return

    if tlpstat_cmd == None:
        textbuffer.set_text('tlp-stat executable not found.')
        return

    tlpstat = check_output([sudo_cmd, "tlp-stat"]).decode(sys.stdout.encoding)
    textbuffer.set_text(tlpstat)


def create_stat_box() -> Gtk.Box:
    scrolledwindow = Gtk.ScrolledWindow()
    scrolledwindow.set_hexpand(True)
    scrolledwindow.set_vexpand(True)

    textbuffer = Gtk.TextBuffer()
    textbuffer.set_text('Click fetch button to receive results')

    textview = Gtk.TextView()
    textview.set_buffer(textbuffer)
    textview.set_editable(False)

    scrolledwindow.add(textview)

    emptylabel = Gtk.Label()

    fetchbutton = Gtk.Button(label=' Fetch stats', image=Gtk.Image(stock=Gtk.STOCK_CONVERT))
    fetchbutton.connect('clicked', fetch_tlp_stat, textbuffer)

    buttonbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    buttonbox.pack_start(emptylabel, True, True, 0)
    buttonbox.pack_start(fetchbutton, False, False, 0)

    statbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    statbox.set_margin_top(18)
    statbox.set_margin_bottom(18)
    statbox.set_margin_left(18)
    statbox.set_margin_right(18)
    statbox.pack_start(buttonbox, False, False, 0)
    statbox.pack_start(scrolledwindow, True, True, 0)

    return statbox