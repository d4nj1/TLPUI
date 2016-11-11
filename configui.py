import gettext
import configparser 
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from collections import OrderedDict

from ui_config_objects import gtkswitch, gtkentry, gtkselection, gtkcheckbutton, gtkspinbutton, gtktoggle
from file import get_json_schema_object

config = configparser.ConfigParser()
config.read('app.ini')
lang = []
lang.append(config['locale']['lang'])

trans = gettext.translation('configdescriptions', 'lang/', languages=lang)
T_ = trans.gettext


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


def create_config_widget(objecttype, objectvalues, tlpobject) -> Gtk.Widget:
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

    return configwidget


def create_item_box(configobjects, doc, grouptitle) -> Gtk.Box:
    configuibox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

    if len(configobjects) > 1:
        transgrouptitle = grouptitle + "__GROUP_TITLE"
        grouplabel = Gtk.Label()
        grouplabel.set_markup(' <b>' + T_(transgrouptitle) + '</b> ')
        grouplabel.set_use_markup(True)
        grouplabel.set_margin_bottom(12)
        grouplabel.set_halign(Gtk.Align.START)
        grouplabel.set_valign(Gtk.Align.START)

        configuibox.pack_start(grouplabel, False, False, 0)

    for configobject in configobjects:
        tlpobject = configobject[0]

        tlpuiobject = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)
        tlpuiobject.set_margin_left(18)
        tlpuiobject.set_margin_right(18)

        statetogglebox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        tlpconfigbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # on/off state
        toggle = gtktoggle.create_toggle_button(tlpobject, tlpconfigbox)
        statetogglebox.pack_start(toggle, False, False, 0)
        statetogglebox.set_halign(Gtk.Align.CENTER)
        statetogglebox.set_valign(Gtk.Align.CENTER)

        # horizontal separator
        hseparator = Gtk.HSeparator()

        # specific config gtk object
        configwidget = create_config_widget(configobject[1], configobject[2], tlpobject)
        configwidget.set_margin_top(6)
        configwidget.set_margin_bottom(6)
        configwidget.set_margin_left(6)

        # object label
        configname = tlpobject.get_name()
        transconfigtitle = configname + "__ID_TITLE"
        configlabel = Gtk.Label(xalign=0)
        configlabel.set_markup(' <b>' + T_(transconfigtitle) + '</b> ')
        configlabel.set_use_markup(True)
        configlabel.set_size_request(300, 0)

        # combine boxes
        tlpconfigbox.pack_start(configlabel, False, False, 0)
        tlpconfigbox.pack_start(configwidget, True, True, 0)

        if configname.endswith('_BAT'):
            image = Gtk.Image.new_from_file('icons/OnBAT.svg')
            tlpconfigbox.pack_start(image, False, False, 12)
        elif configname.endswith('_AC'):
            image = Gtk.Image.new_from_file('icons/OnAC.svg')
            tlpconfigbox.pack_start(image, False, False, 12)

        tlpuiobject.pack_start(statetogglebox, False, False, 0)
        tlpuiobject.pack_start(tlpconfigbox, False, False, 0)

        configuibox.pack_start(tlpuiobject, True, True, 0)

    # object description
    configdescriptionlabel = Gtk.Label()
    configdescriptionlabel.set_markup(doc)
    configdescriptionlabel.set_line_wrap(True)
    configdescriptionlabel.set_margin_top(6)
    configdescriptionlabel.set_margin_bottom(12)
    configdescriptionlabel.set_margin_left(48)
    configdescriptionlabel.set_halign(Gtk.Align.START)
    configdescriptionlabel.set_valign(Gtk.Align.START)

    configuibox.pack_start(configdescriptionlabel, True, True, 0)
    configuibox.pack_start(hseparator, True, True, 0)

    return configuibox


def get_tlp_categories(tlpconfig) -> OrderedDict:
    propertyobjects = OrderedDict()
    categories = get_json_schema_object('categories')

    for category in categories:
        categorybox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)

        configs = category['configs']
        for config in configs:
            grouptitle = ""
            configobjects = list()

            if 'group' in config:
                grouptitle = config['group']
                transdescription = grouptitle + "__GROUP_DESCRIPTION"
                groupitems = config['ids']
                for groupitem in groupitems:
                    id = groupitem['id']
                    type = groupitem['type']
                    values = groupitem['values']

                    tlpitem = tlpconfig[id]
                    configobjects.append([tlpitem, type, values])
            else:
                id = config['id']
                transdescription = id + "__ID_DESCRIPTION"
                type = config['type']
                values = config['values']

                tlpitem = tlpconfig[id]
                configobjects.append([tlpitem, type, values])

            description = T_(transdescription)

            configbox = create_item_box(configobjects, description, grouptitle)
            configbox.set_margin_left(12)
            configbox.set_margin_right(12)
            configbox.set_margin_top(12)
            categorybox.pack_start(configbox, False, False, 0)

        transcategory = category['name'] + "__CATEGORY_TITLE"
        categorylabel = T_(transcategory)
        propertyobjects[categorylabel] = categorybox

    return propertyobjects
