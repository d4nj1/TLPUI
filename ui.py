from gi.repository import Gtk, Gdk
from collections import OrderedDict
from io import open
from json import load

from ui_config_objects import gtkswitch, gtkentry, gtkselection, gtkcheckbutton, gtkspinbutton, gtktoggle
from file import read_tlp_file_config, write_tlp_file_config
from config import get_changed_properties


def close_window(self, event):
    # ctrl+q or ctrl+w
    if event.state & Gdk.ModifierType.CONTROL_MASK and (event.keyval == 113 or event.keyval == 119):
        if self.get_name() == 'GtkWindow':
            Gtk.main_quit()
        else:
            self.destroy()


def create_config_ui_box(tlpobject, objecttype, objectvalues, doc) -> Gtk.Frame:
    tlpconfigframe = Gtk.Frame()
    tlpuiobject = Gtk.Box()

    framelabel = Gtk.Label(' <b>' + tlpobject.get_name() + '</b> ')
    framelabel.set_use_markup(True)

    tlpconfigframe.set_label_widget(framelabel)
    tlpconfigframe.set_label_align(0, 0.5)

    tlpswitchbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    tlpconfigbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

    # on/off state
    toggle = gtktoggle.create_toggle_button(tlpobject, tlpconfigbox)
    tlpswitchbox.pack_start(toggle, False, False, 0)
    tlpswitchbox.set_halign(Gtk.Align.CENTER)
    tlpswitchbox.set_valign(Gtk.Align.CENTER)

    # vertical separator
    separator = Gtk.VSeparator()

    # specific config gtk object
    configuiobject = Gtk.Widget

    if (objecttype == 'entry'):
        configuiobject = gtkentry.create_entry(tlpobject)
    elif (objecttype == 'bselect'):
        configuiobject = gtkswitch.create_state_switch(objectvalues, tlpobject)
    elif (objecttype == 'select'):
        configuiobject = gtkselection.create_selection_box(objectvalues, tlpobject)
    elif (objecttype == 'check'):
        configuiobject = gtkcheckbutton.create_checkbutton_box(objectvalues, tlpobject)
    elif (objecttype == 'numeric'):
        configuiobject = gtkspinbutton.create_numeric_spinbutton(objectvalues, tlpobject)

    configuiobject.set_margin_top(10)
    configuiobject.set_margin_bottom(5)
    configuiobject.set_halign(Gtk.Align.START)
    configuiobject.set_valign(Gtk.Align.START)

    # object label and description
    doclabel = Gtk.Label('<i><small>' + doc + '</small></i>', xalign=0)
    doclabel.set_line_wrap(True)
    doclabel.set_use_markup(True)
    doclabel.set_margin_bottom(10)

    tlpconfigbox.pack_start(configuiobject, True, True, 0)
    tlpconfigbox.pack_start(doclabel, True, True, 0)

    tlpuiobject.pack_start(tlpswitchbox, False, False, 20)
    tlpuiobject.pack_start(separator, False, False, 0)
    tlpuiobject.pack_start(tlpconfigbox, True, True, 20)
    tlpconfigframe.add(tlpuiobject)

    return tlpconfigframe


def create_tlp_ui_categories(tlpconfig) -> OrderedDict:
    propertyobjects = OrderedDict()
    jsonfile = open('configcategories.json')
    jsonobject = load(jsonfile)

    categories = jsonobject['categories']

    for category in categories:
        label = category['name']
        categorybox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        configs = category['configs']
        for config in configs:
            id = config['id']
            type = config['type']
            values = config['values']
            description = config['description']

            for item in tlpconfig:
                configid = item.get_name()
                if configid == id:
                    configbox = create_config_ui_box(item, type, values, description)
                    configbox.set_margin_left(15)
                    configbox.set_margin_right(15)
                    configbox.set_margin_top(15)
                    categorybox.pack_start(configbox, False, False, 0)

        propertyobjects[label] = categorybox

    return propertyobjects


def open_file_chooser(self, fileentry):
    filechooser = Gtk.FileChooserDialog('Choose config file', None, Gtk.FileChooserAction.OPEN, (
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    filechooser.set_local_only(True)

    response = filechooser.run()
    if response == Gtk.ResponseType.OK:
        filepath = filechooser.get_filename()
        fileentry.set_text(filepath)
    filechooser.destroy()


def load_tlp_config(self, filenamepointer, window):
    filename = filenamepointer()
    tlpconfig = read_tlp_file_config(filename)

    newContentBox = create_content_box(window, filename, tlpconfig)
    children = window.get_children()
    for child in children:
        window.remove(child)
    window.add(newContentBox)
    window.show_all()


def save_tlp_config(self, filenamepointer, tlpconfig, window):
    changedproperties = get_changed_properties(tlpconfig)

    dialog = Gtk.MessageDialog()
    dialog.set_default_size(150, 100)
    dialog.connect('key-press-event', close_window)

    if len(changedproperties) == 0:
        dialog.format_secondary_markup('<b>No changes</b>')
    else:
        infotext = '<b>Changed values:</b>\n'
        for property in changedproperties:
            infotext += '<small>' + property[0] + ' -> ' + property[2] + '</small>\n'

        dialog.format_secondary_markup(infotext.rstrip())
        filename = filenamepointer()
        write_tlp_file_config(changedproperties, filename)

        # reload config after file save
        load_tlp_config(self, filenamepointer, window)

    dialog.run()
    dialog.destroy()


def create_settings_box(window, configpath, tlp_config_items):
    fileentry = Gtk.Entry()
    fileentry.set_editable(False)
    fileentry.set_text(configpath)
    fileentry.connect('changed', load_tlp_config, fileentry.get_text, window)

    filebutton = Gtk.Button(label=' Open', image=Gtk.Image(stock=Gtk.STOCK_OPEN))
    filebutton.connect('clicked', open_file_chooser, fileentry)

    reloadbutton = Gtk.Button(label=' Reload', image=Gtk.Image(stock=Gtk.STOCK_REFRESH))
    reloadbutton.connect('clicked', load_tlp_config, fileentry.get_text, window)
    savebutton = Gtk.Button(label=' Save', image=Gtk.Image(stock=Gtk.STOCK_SAVE))
    savebutton.connect('clicked', save_tlp_config, fileentry.get_text, tlp_config_items, window)

    settingsbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    settingsbox.pack_start(filebutton, False, False, 2)
    settingsbox.pack_start(fileentry, True, True, 2)
    settingsbox.pack_start(reloadbutton, False, False, 2)
    settingsbox.pack_start(savebutton, False, False, 2)

    return settingsbox


def create_config_box(tlp_config_items) -> Gtk.Box:
    notebook = Gtk.Notebook()
    notebook.set_tab_pos(Gtk.PositionType.TOP)

    ui_categories = create_tlp_ui_categories(tlp_config_items)
    for label, configitem in ui_categories.items():
        categorylabel = Gtk.Label('<small>' + label + '</small>')
        categorylabel.set_use_markup(True)
        categorylabel.set_margin_left(10)
        categorylabel.set_margin_right(10)

        viewport = Gtk.Viewport()
        viewport.set_name('categoryViewport')
        viewport.add(configitem)

        scroll = Gtk.ScrolledWindow()
        scroll.add(viewport)

        notebook.append_page(scroll, categorylabel)

    containerbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    containerbox.pack_start(notebook, True, True, 2)

    return containerbox


def create_content_box(window, configpath, tlp_config_items) -> Gtk.Box:
    settingsbox = create_settings_box(window, configpath, tlp_config_items)
    configbox = create_config_box(tlp_config_items)

    contentbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    contentbox.pack_start(settingsbox, False, False, 2)
    contentbox.pack_start(configbox, True, True, 2)

    return contentbox