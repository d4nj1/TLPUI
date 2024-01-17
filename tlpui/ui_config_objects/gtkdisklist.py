"""Disk settings UI widget."""

from gi.repository import Gtk

from collections import OrderedDict
from ..uihelper import get_theme_image
from .. import mainui
from .. import file
from .. import settings
from .. import settingshelper


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

    configranges = get_disk_config_ranges()
    existingdisks = read_existing_disk_config()

    disks = OrderedDict()
    keeps = OrderedDict()
    disklist = settingshelper.exec_command(["tlp", "diskid"])
    for line in disklist.splitlines():
        diskid = line.split(':')[0].lstrip().rstrip()

        diskvalues = get_disk_values(diskid, existingdisks)
        defaultvalues = diskvalues[0]
        keepvalues = diskvalues[1]

        notebookgrid = Gtk.Grid()
        notebookgrid.set_row_homogeneous(True)
        notebookgrid.set_column_spacing(12)

        configlabel = Gtk.Label(label='Config', halign=Gtk.Align.START)
        valuelabel = Gtk.Label(label='Value', halign=Gtk.Align.START)
        keeplabel = Gtk.Label(label='Hardware default', halign=Gtk.Align.START)

        apmlevelonaclabel = Gtk.Label(label='DISK_APM_LEVEL_ON_AC', halign=Gtk.Align.START)
        apmlevelonacspiner = create_spinbutton(configranges[0], int(defaultvalues[0]))
        apmlevelonackeep = create_keep(apmlevelonacspiner, keepvalues[0])

        apmlevelonbatlabel = Gtk.Label(label='DISK_APM_LEVEL_ON_BAT', halign=Gtk.Align.START)
        apmlevelonbatspiner = create_spinbutton(configranges[1], int(defaultvalues[1]))
        apmlevelonbatkeep = create_keep(apmlevelonbatspiner, keepvalues[1])

        spindowntimeoutonaclabel = Gtk.Label(label='DISK_SPINDOWN_TIMEOUT_ON_AC', halign=Gtk.Align.START)
        spindowntimeoutonacspiner = create_spinbutton(configranges[2], int(defaultvalues[2]))
        spindowntimeoutonackeep = create_keep(spindowntimeoutonacspiner, keepvalues[2])

        spindowntimeoutonbatlabel = Gtk.Label(label='DISK_SPINDOWN_TIMEOUT_ON_BAT', halign=Gtk.Align.START)
        spindowntimeoutonbatspiner = create_spinbutton(configranges[3], int(defaultvalues[3]))
        spindowntimeoutonbatkeep = create_keep(spindowntimeoutonbatspiner, keepvalues[3])

        ioschedlabel = Gtk.Label(label='DISK_IOSCHED', halign=Gtk.Align.START)
        ioschedselect = create_selectbox(configranges[4], defaultvalues[4])
        ioschedkeep = create_keep(ioschedselect, keepvalues[4])

        notebookgrid.attach(Gtk.Label(' '), 0, 0, 1, 1)
        notebookgrid.attach(configlabel, 1, 0, 1, 1)
        notebookgrid.attach(valuelabel, 2, 0, 1, 1)
        notebookgrid.attach(keeplabel, 3, 0, 1, 1)
        notebookgrid.attach(Gtk.Label(' '), 4, 0, 1, 1)

        notebookgrid.attach(apmlevelonaclabel, 1, 1, 1, 1)
        notebookgrid.attach(apmlevelonacspiner, 2, 1, 1, 1)
        notebookgrid.attach(apmlevelonackeep, 3, 1, 1, 1)

        notebookgrid.attach(apmlevelonbatlabel, 1, 2, 1, 1)
        notebookgrid.attach(apmlevelonbatspiner, 2, 2, 1, 1)
        notebookgrid.attach(apmlevelonbatkeep, 3, 2, 1, 1)

        notebookgrid.attach(spindowntimeoutonaclabel, 1, 3, 1, 1)
        notebookgrid.attach(spindowntimeoutonacspiner, 2, 3, 1, 1)
        notebookgrid.attach(spindowntimeoutonackeep, 3, 3, 1, 1)

        notebookgrid.attach(spindowntimeoutonbatlabel, 1, 4, 1, 1)
        notebookgrid.attach(spindowntimeoutonbatspiner, 2, 4, 1, 1)
        notebookgrid.attach(spindowntimeoutonbatkeep, 3, 4, 1, 1)

        notebookgrid.attach(ioschedlabel, 1, 5, 1, 1)
        notebookgrid.attach(ioschedselect, 2, 5, 1, 1)
        notebookgrid.attach(ioschedkeep, 3, 5, 1, 1)

        notebooklabel = Gtk.Label(diskid)
        notebook.append_page(notebookgrid, notebooklabel)

        disks[diskid] = [apmlevelonacspiner,
                         apmlevelonbatspiner,
                         spindowntimeoutonacspiner,
                         spindowntimeoutonbatspiner,
                         ioschedselect]
        keeps[diskid] = [apmlevelonackeep,
                         apmlevelonbatkeep,
                         spindowntimeoutonackeep,
                         spindowntimeoutonbatkeep,
                         ioschedkeep]

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
        diskdevices = ''
        apmlevelonac = ''
        apmlevelonbat = ''
        spindowntimeoutonac = ''
        spindowntimeoutonbat = ''
        iosched = ''

        for key, value in disks.items():
            diskdevices = diskdevices + ' ' + key
            keep = keeps[key]
            apmlevelonac = f'{apmlevelonac} {get_keep_value(keep[0], str(value[0].get_value_as_int()))}'
            apmlevelonbat = f'{apmlevelonbat} {get_keep_value(keep[1], str(value[1].get_value_as_int()))}'
            spindowntimeoutonac = f'{spindowntimeoutonac} {get_keep_value(keep[2], str(value[2].get_value_as_int()))}'
            spindowntimeoutonbat = f'{spindowntimeoutonbat} {get_keep_value(keep[3], str(value[3].get_value_as_int()))}'
            iosched = f'{iosched} {get_keep_value(keep[4], value[4].get_active_text())}'

        set_tlp_value('DISK_DEVICES', diskdevices.lstrip())
        set_tlp_value('DISK_APM_LEVEL_ON_AC', apmlevelonac.lstrip())
        set_tlp_value('DISK_APM_LEVEL_ON_BAT', apmlevelonbat.lstrip())
        set_tlp_value('DISK_SPINDOWN_TIMEOUT_ON_AC', spindowntimeoutonac.lstrip())
        set_tlp_value('DISK_SPINDOWN_TIMEOUT_ON_BAT', spindowntimeoutonbat.lstrip())
        set_tlp_value('DISK_IOSCHED', iosched.lstrip())

        mainui.load_tlp_config(self, window, False)

    dialog.destroy()


def get_keep_value(keep: Gtk.CheckButton, value: str):
    """Set keep value."""
    return 'keep' if keep.get_active() else value


def set_tlp_value(configname: str, value: str):
    """Store applied config changes."""
    settings.tlpconfig[configname].set_value(value)


def get_disk_values(diskid: str, existingdisks: OrderedDict):
    """Read disk value config."""
    defaultvalues = ['254', '128', '0', '0', 'cfq']
    keepvalues = [False, False, False, False, False]
    if diskid in existingdisks.keys():
        existingvalues = existingdisks[diskid]
        for index in range(0, 5):
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


def read_existing_disk_config() -> OrderedDict:
    """Fetch disk config from TLP."""
    devices = settings.tlpconfig['DISK_DEVICES'].get_value().split(' ')
    apmlevelonac = settings.tlpconfig['DISK_APM_LEVEL_ON_AC'].get_value().split(' ')
    apmlevelonbat = settings.tlpconfig['DISK_APM_LEVEL_ON_BAT'].get_value().split(' ')
    spindowntimeoutonac = settings.tlpconfig['DISK_SPINDOWN_TIMEOUT_ON_AC'].get_value().split(' ')
    spindowntimeoutonbat = settings.tlpconfig['DISK_SPINDOWN_TIMEOUT_ON_BAT'].get_value().split(' ')
    iosched = settings.tlpconfig['DISK_IOSCHED'].get_value().split(' ')

    existingdiskconfig = OrderedDict()
    index = 0
    for device in devices:
        existingdiskconfig[device] = [apmlevelonac[index],
                                      apmlevelonbat[index],
                                      spindowntimeoutonac[index],
                                      spindowntimeoutonbat[index],
                                      iosched[index]]
        index += 1

    return existingdiskconfig


def get_disk_config_ranges():
    """Get setting ranges for disk configs."""
    apmlevelrangeac = ''
    apmlevelrangebat = ''
    spindownrangetimeoutac = ''
    spindownrangetimeoutbat = ''
    ioschedvalues = ''

    categories = file.get_yaml_schema_object('categories')
    for category in categories:
        if category['name'] != 'Disks':
            continue

        for config in category['configs']:
            if 'group' in config:
                if config['group'] == 'DISK_APM_LEVEL':
                    for item in config['ids']:
                        if item['id'] == 'DISK_APM_LEVEL_ON_AC':
                            apmlevelrangeac = item['values']
                        elif item['id'] == 'DISK_APM_LEVEL_ON_BAT':
                            apmlevelrangebat = item['values']
                elif config['group'] == 'DISK_SPINDOWN_TIMEOUT':
                    for item in config['ids']:
                        if item['id'] == 'DISK_SPINDOWN_TIMEOUT_ON_AC':
                            spindownrangetimeoutac = item['values']
                        elif item['id'] == 'DISK_SPINDOWN_TIMEOUT_ON_BAT':
                            spindownrangetimeoutbat = item['values']
            else:
                if config['id'] == 'DISK_IOSCHED':
                    ioschedvalues = config['values']

    return [apmlevelrangeac, apmlevelrangebat, spindownrangetimeoutac, spindownrangetimeoutbat, ioschedvalues]
