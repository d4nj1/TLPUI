"""Usb settings UI widget."""

import re
from gi.repository import Gtk

from collections import OrderedDict
from .. import settings
from .. import settingshelper
from ..uihelper import get_theme_image

global indexstore


def create_list(configname: str, window: Gtk.Window) -> Gtk.Box:
    """Create usb list button."""
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    label = Gtk.Label(settings.tlpconfig[configname].get_value().replace(" ", "\n"))

    button = Gtk.Button(label=' Edit', image=get_theme_image('edit-symbolic', Gtk.IconSize.BUTTON))
    button.connect('clicked', edit_list, configname, label, window)
    button.set_always_show_image(True)

    box.pack_start(label, False, False, 0)
    box.pack_start(button, False, False, 12)
    return box


def edit_list(self, configname: str, usblistlabel: Gtk.Label, window: Gtk.Window):
    """Create usb list view."""
    tlpobject = settings.tlpconfig[configname]
    usblistpattern = re.compile(r'^.+?([a-f\d]{4}:[a-f\d]{4})(.+?)$')
    currentitems = OrderedDict()
    if tlpobject.get_value() != '':
        for item in tlpobject.get_value().split(' '):
            currentitems[item] = ["", True]

    tlpusblist = settingshelper.exec_command(["lsusb"])

    usbitems = OrderedDict()
    for line in tlpusblist.splitlines():
        matcher = usblistpattern.match(line)
        usbid = matcher.group(1)
        description = matcher.group(2)
        active = False

        # only add usb id once
        if usbid in usbitems:
            continue

        # check if item is selected
        if usbid in currentitems:
            active = True
            del currentitems[usbid]
        usbitems[usbid] = [description, active]

    usbitems.update(currentitems)

    grid = Gtk.Grid()
    grid.set_row_homogeneous(True)
    grid.set_column_spacing(12)

    grid.attach(Gtk.Label(''), 0, 0, 1, 1)
    grid.attach(Gtk.Label(label='ID', halign=Gtk.Align.START), 1, 0, 1, 1)
    grid.attach(Gtk.Label(label='Description', halign=Gtk.Align.START), 2, 0, 1, 1)
    grid.attach(Gtk.Label(''), 3, 0, 1, 1)

    rowindex = 2
    allitems = list()
    selecteditems = list()
    for key, value in usbitems.items():
        allitems.append(key)
        toggle = Gtk.ToggleButton(key)
        toggle.connect('toggled', on_button_toggled, key, selecteditems)

        if value[1]:
            toggle.set_active(True)

        label = Gtk.Label(value[0])
        label.set_halign(Gtk.Align.START)

        grid.attach(toggle, 1, rowindex, 1, 1)
        grid.attach(label, 2, rowindex, 1, 1)

        rowindex += 1

    addbutton = Gtk.Button(label=' Add', image=get_theme_image('list-add-symbolic', Gtk.IconSize.BUTTON))
    addbutton.set_sensitive(False)
    addbutton.set_always_show_image(True)

    addentry = Gtk.Entry()
    addentry.set_width_chars(9)
    addentry.set_max_length(9)
    addentry.connect('changed', usb_entry_check, addbutton)

    addbutton.connect('clicked', add_usb_item, addentry, grid, allitems, selecteditems)

    addlabel = Gtk.Label(label='Add custom unattached USB IDs:', halign=Gtk.Align.START)

    addbox = Gtk.Box()
    addbox.pack_start(addentry, False, False, 0)
    addbox.pack_start(addbutton, False, False, 12)
    addbox.pack_start(Gtk.Label(''), True, True, 0)

    grid.attach(addlabel, 1, rowindex, 2, 1)
    grid.attach(addbox, 1, rowindex + 1, 2, 1)

    global indexstore
    indexstore = rowindex + 2

    dialog = Gtk.Dialog('Usb devices', window, 0, (
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OK, Gtk.ResponseType.OK
    ))

    contentarea = dialog.get_content_area()
    contentarea.set_spacing(6)
    contentarea.add(grid)
    dialog.show_all()

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        configvalue = ' '.join(str(item) for item in selecteditems)
        tlpobject.set_value(configvalue)
        usblistlabel.set_text(configvalue.replace(" ", "\n"))

    dialog.destroy()


def on_button_toggled(self: Gtk.ToggleButton, key: str, selecteditems: list):
    """Change visibility on toggle."""
    if self.get_active():
        selecteditems.append(key)
    else:
        selecteditems.remove(key)


def usb_entry_check(self: Gtk.Entry, button: Gtk.Button):
    """Validate usb entries."""
    usbpattern = re.compile(r'^[a-f\d]{4}:[a-f\d]{4}$')
    if usbpattern.match(self.get_text()):
        self.set_name('validEntry')
        button.set_sensitive(True)
    else:
        self.set_name('invalidEntry')
        button.set_sensitive(False)


def add_usb_item(self, entry: Gtk.Entry, grid: Gtk.Grid, allitems: list, selecteditems: list):
    """Add usb config item."""
    key = entry.get_text()
    if key in allitems:
        return
    allitems.append(key)

    toggle = Gtk.ToggleButton(key)
    toggle.connect('toggled', on_button_toggled, key, selecteditems)
    toggle.set_active(True)

    label = Gtk.Label('')
    label.set_halign(Gtk.Align.START)

    global indexstore
    grid.attach(toggle, 1, indexstore, 1, 1)
    grid.attach(label, 2, indexstore, 1, 1)

    indexstore += 1
    grid.show_all()
