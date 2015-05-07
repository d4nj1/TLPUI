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


def create_config_ui_box(tlpobject, objecttype, objectvalues, doc) -> Gtk.Box:
    tlpuiobject = Gtk.Box()

    configuibox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    statetogglebox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    tlpconfigbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

    # on/off state
    toggle = gtktoggle.create_toggle_button(tlpobject, tlpconfigbox)
    statetogglebox.pack_start(toggle, False, False, 0)
    statetogglebox.set_halign(Gtk.Align.CENTER)
    statetogglebox.set_valign(Gtk.Align.CENTER)

    # vertical separator
    vseparator = Gtk.VSeparator()

    # horizontal separator
    hseparator = Gtk.HSeparator()

    # specific config gtk object
    configwidget = Gtk.Widget

    if (objecttype == 'entry'):
        configwidget = gtkentry.create_entry(tlpobject)
    elif (objecttype == 'bselect'):
        configwidget = gtkswitch.create_state_switch(objectvalues, tlpobject)
    elif (objecttype == 'select'):
        configwidget = gtkselection.create_selection_box(objectvalues, tlpobject)
    elif (objecttype == 'check'):
        configwidget = gtkcheckbutton.create_checkbutton_box(objectvalues, tlpobject)
    elif (objecttype == 'numeric'):
        configwidget = gtkspinbutton.create_numeric_spinbutton(objectvalues, tlpobject)

    configwidget.set_margin_top(10)
    configwidget.set_margin_bottom(5)
    configwidget.set_halign(Gtk.Align.START)
    configwidget.set_valign(Gtk.Align.START)

    # object label
    configlabel = Gtk.Label(' <b>' + tlpobject.get_name() + '</b> ', xalign=0)
    configlabel.set_use_markup(True)
    configlabel.set_margin_bottom(5)

    # object description
    configdescriptionlabel = Gtk.Label('<i><small>' + doc + '</small></i>', xalign=0)
    configdescriptionlabel.set_line_wrap(True)
    configdescriptionlabel.set_use_markup(True)
    configdescriptionlabel.set_margin_bottom(10)

    # combine boxes
    tlpconfigbox.pack_start(configwidget, True, True, 0)
    tlpconfigbox.pack_start(configdescriptionlabel, True, True, 0)

    tlpuiobject.pack_start(statetogglebox, False, False, 20)
    tlpuiobject.pack_start(vseparator, False, False, 0)
    tlpuiobject.pack_start(tlpconfigbox, True, True, 20)

    configuibox.pack_start(configlabel, False, False, 0)
    configuibox.pack_start(tlpuiobject, True, True, 0)
    configuibox.pack_start(hseparator, True, True, 0)

    return configuibox


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


def fetch_tlp_stat(self, textbuffer):
    textbuffer.set_text('button clicked, further implementation needed')


def create_settings_box(window, configpath, tlp_config_items):
    fileentry = Gtk.Label(configpath)
    fileentry.set_alignment(0, 0.5)

    filebutton = Gtk.Button(label=' Open', image=Gtk.Image(stock=Gtk.STOCK_OPEN))
    filebutton.connect('clicked', open_file_chooser, fileentry)

    reloadbutton = Gtk.Button(label=' Reload', image=Gtk.Image(stock=Gtk.STOCK_REFRESH))
    reloadbutton.connect('clicked', load_tlp_config, fileentry.get_text, window)
    savebutton = Gtk.Button(label=' Save', image=Gtk.Image(stock=Gtk.STOCK_SAVE))
    savebutton.connect('clicked', save_tlp_config, fileentry.get_text, tlp_config_items, window)

    settingsbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    settingsbox.pack_start(fileentry, True, True, 2)
    settingsbox.pack_start(filebutton, False, False, 2)
    settingsbox.pack_start(reloadbutton, False, False, 2)
    settingsbox.pack_start(savebutton, False, False, 2)

    return settingsbox


def create_config_box(tlp_config_items) -> Gtk.Box:
    notebook = Gtk.Notebook()
    notebook.set_name('configNotebook')
    notebook.set_tab_pos(Gtk.PositionType.LEFT)

    ui_categories = create_tlp_ui_categories(tlp_config_items)
    for label, configitem in ui_categories.items():
        categorylabel = Gtk.Label(label)
        categorylabel.set_alignment(0, 0.5)
        categorylabel.set_margin_top(5)
        categorylabel.set_margin_bottom(5)
        categorylabel.set_margin_left(5)
        categorylabel.set_margin_right(5)

        viewport = Gtk.Viewport()
        viewport.set_name('categoryViewport')
        viewport.add(configitem)

        scroll = Gtk.ScrolledWindow()
        scroll.add(viewport)

        notebook.append_page(scroll, categorylabel)

    containerbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    containerbox.pack_start(notebook, True, True, 2)

    return containerbox


def create_stat_box() -> Gtk.Box:
    textbuffer = Gtk.TextBuffer()
    textbuffer.set_text('Click button to receive results')

    textview = Gtk.TextView()
    textview.set_buffer(textbuffer)

    emptylabel = Gtk.Label()

    fetchbutton = Gtk.Button(label=' Fetch stats', image=Gtk.Image(stock=Gtk.STOCK_REFRESH))
    fetchbutton.connect('clicked', fetch_tlp_stat, textbuffer)

    buttonbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    buttonbox.pack_start(emptylabel, True, True, 2)
    buttonbox.pack_start(fetchbutton, False, False, 2)

    statbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    statbox.set_margin_top(10)
    statbox.set_margin_bottom(10)
    statbox.set_margin_left(10)
    statbox.set_margin_right(10)
    statbox.pack_start(buttonbox, False, False, 5)
    statbox.pack_start(textview, True, True, 0)

    return statbox


def create_content_box(window, configpath, tlp_config_items) -> Gtk.Box:
    notebook = Gtk.Notebook()
    notebook.set_tab_pos(Gtk.PositionType.TOP)

    settingsbox = create_settings_box(window, configpath, tlp_config_items)
    configbox = create_config_box(tlp_config_items)

    contentbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    contentbox.set_margin_top(10)
    contentbox.set_margin_bottom(10)
    contentbox.set_margin_left(10)
    contentbox.set_margin_right(10)
    contentbox.pack_start(settingsbox, False, False, 5)
    contentbox.pack_start(configbox, True, True, 0)

    configlabel = Gtk.Label('TLP config')
    configlabel.set_hexpand(True)

    statlabel = Gtk.Label('TLP stat')
    statlabel.set_hexpand(True)

    statbox = create_stat_box()

    notebook.append_page(contentbox, configlabel)
    notebook.append_page(statbox, statlabel)

    mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    mainbox.pack_start(notebook, True, True, 0)

    return mainbox