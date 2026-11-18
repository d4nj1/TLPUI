"""Disk settings UI widget."""

from gi.repository import Gtk

from collections import OrderedDict
from ..uihelper import get_theme_image
from .. import mainui
from .. import file
from .. import settings
from .. import settingshelper


def get_profile_suffixes() -> list:
    """Determine profile suffixes of disk parameters from the loaded TLP config.
    TLP 1.11 renamed _AC/_BAT to _PRF/_BAL and added _SAV variants."""
    if 'DISK_APM_LEVEL_ON_PRF' in settings.tlpconfig:
        suffixes = ['PRF', 'BAL']
        if 'DISK_APM_LEVEL_ON_SAV' in settings.tlpconfig:
            suffixes.append('SAV')
    else:
        suffixes = ['AC', 'BAT']
    return suffixes


def get_disk_config_names() -> list:
    """Disk config names in dialog row order."""
    suffixes = get_profile_suffixes()
    confignames = [f'DISK_APM_LEVEL_ON_{suffix}' for suffix in suffixes]
    confignames += [f'DISK_SPINDOWN_TIMEOUT_ON_{suffix}' for suffix in suffixes]
    confignames.append('DISK_IOSCHED')
    return confignames


def get_default_value(configname: str) -> str:
    """Fallback value for yet unconfigured disks."""
    if configname.startswith('DISK_APM_LEVEL'):
        return '254' if configname.endswith(('_AC', '_PRF')) else '128'
    if configname.startswith('DISK_SPINDOWN_TIMEOUT'):
        return '0'
    return 'cfq'


def create_list(configname: str, window: Gtk.Window) -> Gtk.Box:
    """Create disk list button."""
    tlpobject = settings.tlpconfig[configname]
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    label = Gtk.Label(tlpobject.get_value())
    label.set_width_chars(len(tlpobject.get_value()) + 5)

    button = Gtk.Button(label=' Edit', image=get_theme_image('edit-symbolic', Gtk.IconSize.BUTTON))
    button.connect('clicked', edit_list, window)
    button.set_always_show_image(True)

    box.pack_start(label, False, False, 0)
    box.pack_start(button, False, False, 12)
    return box


def edit_list(self: Gtk.Button, window: Gtk.Window):
    """Create disk list view."""
    notebook = Gtk.Notebook()
    notebook.set_tab_pos(Gtk.PositionType.TOP)

    confignames = get_disk_config_names()
    configranges = get_disk_config_ranges(confignames)
    existingdisks = read_existing_disk_config(confignames)

    disks = OrderedDict()
    keeps = OrderedDict()
    disklist = settingshelper.exec_command(["tlp", "diskid"])
    for line in disklist.splitlines():
        diskid = line.split(':')[0].lstrip().rstrip()

        diskvalues = get_disk_values(diskid, confignames, existingdisks)
        defaultvalues = diskvalues[0]
        keepvalues = diskvalues[1]

        notebookgrid = Gtk.Grid()
        notebookgrid.set_row_homogeneous(True)
        notebookgrid.set_column_spacing(12)

        notebookgrid.attach(Gtk.Label(' '), 0, 0, 1, 1)
        notebookgrid.attach(Gtk.Label(label='Config', halign=Gtk.Align.START), 1, 0, 1, 1)
        notebookgrid.attach(Gtk.Label(label='Value', halign=Gtk.Align.START), 2, 0, 1, 1)
        notebookgrid.attach(Gtk.Label(label='Hardware default', halign=Gtk.Align.START), 3, 0, 1, 1)
        notebookgrid.attach(Gtk.Label(' '), 4, 0, 1, 1)

        widgets = []
        keepwidgets = []
        for index, configname in enumerate(confignames):
            configlabel = Gtk.Label(label=configname, halign=Gtk.Align.START)
            if configname == 'DISK_IOSCHED':
                widget = create_selectbox(configranges[index], defaultvalues[index])
            else:
                widget = create_spinbutton(configranges[index], int(defaultvalues[index]))
            keep = create_keep(widget, keepvalues[index])

            notebookgrid.attach(configlabel, 1, index + 1, 1, 1)
            notebookgrid.attach(widget, 2, index + 1, 1, 1)
            notebookgrid.attach(keep, 3, index + 1, 1, 1)

            widgets.append(widget)
            keepwidgets.append(keep)

        notebook.append_page(notebookgrid, Gtk.Label(diskid))

        disks[diskid] = widgets
        keeps[diskid] = keepwidgets

    dialog = Gtk.Dialog('Disk devices', window, 0, (
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OK, Gtk.ResponseType.OK
    ))

    contentarea = dialog.get_content_area()
    contentarea.set_spacing(6)
    contentarea.add(notebook)

    dialog.show_all()

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        diskdevices, newvalues = assemble_config_values(disks, keeps, confignames)
        set_tlp_value('DISK_DEVICES', diskdevices)
        for configname in confignames:
            set_tlp_value(configname, newvalues[configname])

        mainui.load_tlp_config(self, window, False)

    dialog.destroy()


def assemble_config_values(disks: OrderedDict, keeps: OrderedDict, confignames: list):
    """Collect dialog values per disk config item."""
    diskdevices = ''
    newvalues = {configname: '' for configname in confignames}

    for diskid, widgets in disks.items():
        diskdevices = diskdevices + ' ' + diskid
        keep = keeps[diskid]
        for index, configname in enumerate(confignames):
            if configname == 'DISK_IOSCHED':
                value = widgets[index].get_active_text()
            else:
                value = str(widgets[index].get_value_as_int())
            newvalues[configname] = f'{newvalues[configname]} {get_keep_value(keep[index], value)}'

    return diskdevices.lstrip(), {name: value.lstrip() for name, value in newvalues.items()}


def get_keep_value(keep: Gtk.CheckButton, value: str):
    """Set keep value."""
    return 'keep' if keep.get_active() else value


def set_tlp_value(configname: str, value: str):
    """Store applied config changes."""
    settings.tlpconfig[configname].set_value(value)


def get_disk_values(diskid: str, confignames: list, existingdisks: OrderedDict):
    """Read disk value config."""
    defaultvalues = [get_default_value(configname) for configname in confignames]
    keepvalues = [False] * len(confignames)
    if diskid in existingdisks.keys():
        existingvalues = existingdisks[diskid]
        for index in range(len(confignames)):
            if existingvalues[index] == 'keep':
                keepvalues[index] = True
            else:
                defaultvalues[index] = existingvalues[index]
    return defaultvalues, keepvalues


def create_keep(gtkwidget: Gtk.Widget, isactive: bool):
    """Create toggle for keep setting."""
    checkbutton = Gtk.CheckButton(halign=Gtk.Align.CENTER)
    if isactive:
        checkbutton.set_active(True)
        gtkwidget.set_opacity(0.3)

    checkbutton.connect('toggled', on_button_toggled, gtkwidget)
    return checkbutton


def on_button_toggled(self: Gtk.CheckButton, gtkwidget: Gtk.Widget):
    """Change visibility on toggle."""
    if self.get_active():
        gtkwidget.set_opacity(0.3)
    else:
        gtkwidget.set_opacity(1)


def create_spinbutton(values: str, configvalue: str):
    """Create value selector."""
    valuerange = values.split('-')
    adjustment = Gtk.Adjustment(0, float(valuerange[0]), float(valuerange[1]), 1, 10, 0)

    spinbutton = Gtk.SpinButton()
    spinbutton.set_numeric(True)
    spinbutton.set_adjustment(adjustment)
    spinbutton.set_value(float(configvalue))
    return spinbutton


def create_selectbox(values: str, configvalue: str):
    """Create select box."""
    combobox = Gtk.ComboBoxText()
    selectitems = values.split(',')

    countid = 0
    selectid = 0

    for item in selectitems:
        combobox.append_text(item)
        if item in configvalue:
            selectid = countid
        countid += 1

    combobox.set_active(selectid)
    return combobox


def read_existing_disk_config(confignames: list) -> OrderedDict:
    """Fetch disk config from TLP."""
    devices = settings.tlpconfig['DISK_DEVICES'].get_value().split(' ')
    configvalues = [settings.tlpconfig[configname].get_value().split(' ') for configname in confignames]

    existingdiskconfig = OrderedDict()
    for index, device in enumerate(devices):
        existingdiskconfig[device] = [values[index] for values in configvalues]

    return existingdiskconfig


def get_disk_config_ranges(confignames: list) -> list:
    """Get setting ranges for disk configs from the schema."""
    ranges = {configname: '' for configname in confignames}

    categories = file.get_yaml_schema_object('categories')
    for category in categories:
        if category['name'] != 'Disks':
            continue

        for config in category['configs']:
            if 'group' in config:
                for item in config['ids']:
                    if item['id'] in ranges:
                        ranges[item['id']] = item['values']
            elif config['id'] in ranges:
                ranges[config['id']] = config['values']

    return [ranges[configname] for configname in confignames]