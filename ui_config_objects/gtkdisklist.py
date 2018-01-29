import sys
from gi.repository import Gtk

from subprocess import check_output
from collections import OrderedDict
import mainui
import file
import settings


def create_list(tlpobject, window) -> Gtk.Box:
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    label = Gtk.Label(tlpobject.get_value())
    label.set_width_chars(len(tlpobject.get_value())+5)

    button = Gtk.Button(label=' Edit', image=(Gtk.Image(stock=Gtk.STOCK_EDIT)))
    button.connect('clicked', edit_list, window)

    box.pack_start(label, False, False, 0)
    box.pack_start(button, False, False, 12)
    return box


def edit_list(self, window):
    notebook = Gtk.Notebook()
    notebook.set_tab_pos(Gtk.PositionType.TOP)

    configranges = get_disk_config_ranges()
    existingdisks = read_existing_disk_config()

    disks = OrderedDict()
    disklist = check_output(["tlp", "diskid"]).decode(sys.stdout.encoding)
    for line in disklist.splitlines():
        diskid = line.split(':')[0].lstrip().rstrip()

        defaultvalues = [254, 128, 0, 0, 'cfq']
        if diskid in existingdisks.keys():
            defaultvalues = existingdisks[diskid]

        notebookgrid = Gtk.Grid()
        notebookgrid.set_row_homogeneous(True)
        notebookgrid.set_column_spacing(12)

        apmlevelonaclabel = Gtk.Label(label='DISK_APM_LEVEL_ON_AC', halign=Gtk.Align.START)
        apmlevelonacspiner = create_spinbutton(configranges[0], defaultvalues[0])
        apmlevelonbatlabel = Gtk.Label(label='DISK_APM_LEVEL_ON_BAT', halign=Gtk.Align.START)
        apmlevelonbatspiner = create_spinbutton(configranges[1], defaultvalues[1])
        spindowntimeoutonaclabel = Gtk.Label(label='DISK_SPINDOWN_TIMEOUT_ON_AC', halign=Gtk.Align.START)
        spindowntimeoutonacspiner = create_spinbutton(configranges[2], defaultvalues[2])
        spindowntimeoutonbatlabel = Gtk.Label(label='DISK_SPINDOWN_TIMEOUT_ON_BAT', halign=Gtk.Align.START)
        spindowntimeoutonbatspiner = create_spinbutton(configranges[3], defaultvalues[3])
        ioschedlabel = Gtk.Label(label='DISK_IOSCHED', halign=Gtk.Align.START)
        ioschedselect = create_selectbox(configranges[4], defaultvalues[4])

        notebookgrid.attach(apmlevelonaclabel, 0, 0, 1, 1)
        notebookgrid.attach(apmlevelonacspiner, 1, 0, 1, 1)
        notebookgrid.attach(apmlevelonbatlabel, 0, 1, 1, 1)
        notebookgrid.attach(apmlevelonbatspiner, 1, 1, 1, 1)
        notebookgrid.attach(spindowntimeoutonaclabel, 0, 2, 1, 1)
        notebookgrid.attach(spindowntimeoutonacspiner, 1, 2, 1, 1)
        notebookgrid.attach(spindowntimeoutonbatlabel, 0, 3, 1, 1)
        notebookgrid.attach(spindowntimeoutonbatspiner, 1, 3, 1, 1)
        notebookgrid.attach(ioschedlabel, 0, 4, 1, 1)
        notebookgrid.attach(ioschedselect, 1, 4, 1, 1)

        notebooklabel = Gtk.Label(diskid)
        notebook.append_page(notebookgrid, notebooklabel)

        disks[diskid] = [apmlevelonacspiner, apmlevelonbatspiner, spindowntimeoutonacspiner, spindowntimeoutonbatspiner, ioschedselect]

    dialog = Gtk.Dialog('Disk devices', window, 0, (
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OK, Gtk.ResponseType.OK
    ))

    contentarea = dialog.get_content_area()
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
            apmlevelonac = apmlevelonac + ' ' + str(int(value[0].get_value()))
            apmlevelonbat = apmlevelonbat + ' ' + str(int(value[1].get_value()))
            spindowntimeoutonac = spindowntimeoutonac + ' ' + str(int(value[2].get_value()))
            spindowntimeoutonbat = spindowntimeoutonbat + ' ' + str(int(value[3].get_value()))
            iosched = value[4].get_active_text()

        set_tlp_value('DISK_DEVICES', diskdevices.lstrip())
        set_tlp_value('DISK_APM_LEVEL_ON_AC', apmlevelonac.lstrip())
        set_tlp_value('DISK_APM_LEVEL_ON_BAT', apmlevelonbat.lstrip())
        set_tlp_value('DISK_SPINDOWN_TIMEOUT_ON_AC', spindowntimeoutonac.lstrip())
        set_tlp_value('DISK_SPINDOWN_TIMEOUT_ON_BAT', spindowntimeoutonbat.lstrip())
        set_tlp_value('DISK_IOSCHED', iosched.lstrip())

        mainui.load_tlp_config(self, window, False)

    dialog.destroy()


def set_tlp_value(configname, value):
    settings.tlpconfig[configname].set_value(value)


def create_spinbutton(values, configvalue):
    range = values.split('-')
    adjustment = Gtk.Adjustment(0, float(range[0]), float(range[1]), 1, 10, 0)

    spinbutton = Gtk.SpinButton()
    spinbutton.set_numeric(True)
    spinbutton.set_adjustment(adjustment)
    spinbutton.set_value(float(configvalue))
    return spinbutton


def create_selectbox(values, configvalue):
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
    devices = settings.tlpconfig['DISK_DEVICES'].get_value().split(' ')
    apmlevelonac = settings.tlpconfig['DISK_APM_LEVEL_ON_AC'].get_value().split(' ')
    apmlevelonbat = settings.tlpconfig['DISK_APM_LEVEL_ON_BAT'].get_value().split(' ')
    spindowntimeoutonac = settings.tlpconfig['DISK_SPINDOWN_TIMEOUT_ON_AC'].get_value().split(' ')
    spindowntimeoutonbat = settings.tlpconfig['DISK_SPINDOWN_TIMEOUT_ON_BAT'].get_value().split(' ')
    iosched = settings.tlpconfig['DISK_IOSCHED'].get_value().split(' ')

    existingdiskconfig = OrderedDict()
    index = 0
    for device in devices:
        existingdiskconfig[device] = [int(apmlevelonac[index]), int(apmlevelonbat[index]), int(spindowntimeoutonac[index]), int(spindowntimeoutonbat[index]), iosched[index]]
        index+=1

    return existingdiskconfig


def get_disk_config_ranges():
    apmlevelrangeac = ''
    apmlevelrangebat = ''
    spindownrangetimeoutac = ''
    spindownrangetimeoutbat = ''
    ioschedvalues = ''

    categories = file.get_json_schema_object('categories')
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
