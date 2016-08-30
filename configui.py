from collections import OrderedDict
from io import open
from json import load

from gi.repository import Gtk

from ui_config_objects import gtkswitch, gtkentry, gtkselection, gtkcheckbutton, gtkspinbutton, gtktoggle


def create_config_box(tlp_config_items) -> Gtk.Box:
    notebook = Gtk.Notebook()
    notebook.set_name('configNotebook')
    notebook.set_tab_pos(Gtk.PositionType.LEFT)

    tlp_categories = get_tlp_categories(tlp_config_items)
    for label, category in tlp_categories.items():
        categorylabel = Gtk.Label(label)
        categorylabel.set_alignment(1, 0.5)
        categorylabel.set_margin_top(6)
        categorylabel.set_margin_bottom(6)
        categorylabel.set_margin_left(6)
        categorylabel.set_margin_right(6)

        viewport = Gtk.Viewport()
        viewport.set_name('categoryViewport')
        viewport.add(category)

        scroll = Gtk.ScrolledWindow()
        scroll.add(viewport)
        image = Gtk.Image.new_from_file('icons/' + label + '.svg')

        labelbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        labelbox.pack_start(image, False, False, 0)
        labelbox.pack_start(categorylabel, True, True, 0)
        labelbox.show_all()

        notebook.append_page(scroll, labelbox)

    containerbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    containerbox.pack_start(notebook, True, True, 0)

    return containerbox


def create_item_box(tlpobject, objecttype, objectvalues, doc) -> Gtk.Box:
    tlpuiobject = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)
    tlpuiobject.set_margin_left(18)
    tlpuiobject.set_margin_right(18)

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

    configwidget.set_margin_top(6)
    configwidget.set_margin_bottom(6)
    configwidget.set_halign(Gtk.Align.START)
    configwidget.set_valign(Gtk.Align.START)

    # object label
    configlabel = Gtk.Label(' <b>' + tlpobject.get_name() + '</b> ', xalign=0)
    configlabel.set_use_markup(True)
    configlabel.set_margin_bottom(12)

    # object description
    configdescriptionlabel = Gtk.Label('<i><small>' + doc + '</small></i>', xalign=0)
    configdescriptionlabel.set_line_wrap(True)
    configdescriptionlabel.set_use_markup(True)
    configdescriptionlabel.set_margin_bottom(12)

    # combine boxes
    tlpconfigbox.pack_start(configwidget, True, True, 0)
    tlpconfigbox.pack_start(configdescriptionlabel, True, True, 0)

    tlpuiobject.pack_start(statetogglebox, False, False, 0)
    tlpuiobject.pack_start(vseparator, False, False, 0)
    tlpuiobject.pack_start(tlpconfigbox, True, True, 0)

    configuibox.pack_start(configlabel, False, False, 0)
    configuibox.pack_start(tlpuiobject, True, True, 0)
    configuibox.pack_start(hseparator, True, True, 0)

    return configuibox


def get_tlp_categories(tlpconfig) -> OrderedDict:
    propertyobjects = OrderedDict()
    jsonfile = open('configcategories.json')
    jsonobject = load(jsonfile)

    categories = jsonobject['categories']

    for category in categories:
        label = category['name']
        categorybox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)

        configs = category['configs']
        for config in configs:
            id = config['id']
            type = config['type']
            values = config['values']
            description = config['description']

            for item in tlpconfig:
                configid = item.get_name()
                if configid == id:
                    configbox = create_item_box(item, type, values, description)
                    configbox.set_margin_left(12)
                    configbox.set_margin_right(12)
                    configbox.set_margin_top(12)
                    categorybox.pack_start(configbox, False, False, 0)

        propertyobjects[label] = categorybox

    return propertyobjects
