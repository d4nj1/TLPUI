import sys, re
from gi.repository import Gtk

from collections import OrderedDict
from subprocess import check_output


def create_list(tlpobject, window) -> Gtk.Box:
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    label = Gtk.Label(tlpobject.get_value().replace(" ", "\n"))

    button = Gtk.Button(label=' Edit', image=(Gtk.Image(stock=Gtk.STOCK_EDIT)))
    button.connect('clicked', edit_list, tlpobject, label, window)

    box.pack_start(label, False, False, 0)
    box.pack_start(button, False, False, 12)
    return box


def edit_list(self, tlpobject, usblistlabel, window):
    pcilistpattern = re.compile(r'^([a-f\d]{2}:[a-f\d]{2}\.[a-f\d])(.+?)$')
    currentitems = tlpobject.get_value().split(' ')

    tlpusblist = check_output(["lspci"]).decode(sys.stdout.encoding)

    pciitems = OrderedDict()
    for line in tlpusblist.splitlines():
        matcher = pcilistpattern.match(line)
        pciid = matcher.group(1)
        description = matcher.group(2).lstrip()

        pciitems[pciid] = [description, (pciid in currentitems)]

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
    for key, value in pciitems.items():
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

    dialog = Gtk.Dialog('PCI(e) devices', window, 0, (
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


def on_button_toggled(self, key, selecteditems):
    if self.get_active():
        selecteditems.append(key)
    else:
        selecteditems.remove(key)
