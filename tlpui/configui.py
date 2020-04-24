import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from collections import OrderedDict

from . import settings
from . import language
from .ui_config_objects import gtkswitch, gtkentry, gtkselection, gtkmultiselection, gtkcheckbutton, gtkspinbutton, gtktoggle, gtkusblist, gtkpcilist, gtkdisklist, gtkdisklistview
from .file import ConfType, TlpConfig, get_json_schema_object
from .uihelper import get_theme_image, StateImage, EXPECTED_ITEM_MISSING_TEXT


def store_category_num(self, cat, cat_num: int):
    settings.activecategory = cat_num


def create_config_box(window) -> Gtk.Box:
    notebook = Gtk.Notebook()
    notebook.set_name('configNotebook')
    notebook.set_tab_pos(Gtk.PositionType.LEFT)

    categories = get_json_schema_object('categories')
    tlp_categories = get_tlp_categories(window, categories)
    for name, categorydata in tlp_categories.items():
        categorylabel = Gtk.Label(categorydata[0])
        categorylabel.set_alignment(1, 0.5)
        categorylabel.set_margin_top(6)
        categorylabel.set_margin_bottom(6)
        categorylabel.set_margin_left(6)
        categorylabel.set_margin_right(6)

        viewport = Gtk.Viewport()
        viewport.set_name('categoryViewport')
        viewport.add(categorydata[1])

        scroll = Gtk.ScrolledWindow()
        scroll.add(viewport)

        categoryimage = get_theme_image('tlpui-{}-symbolic'.format(name), Gtk.IconSize.MENU)

        labelbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        labelbox.pack_start(categoryimage, False, False, 0)
        labelbox.pack_start(categorylabel, True, True, 0)
        labelbox.show_all()

        notebook.append_page(scroll, labelbox)

    notebook.connect('switch-page', store_category_num)

    containerbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    containerbox.pack_start(notebook, True, True, 0)

    activecategory = settings.activecategory
    notebook.show_all()
    notebook.set_current_page(activecategory)

    return containerbox


def create_config_widget(configname: str, objecttype: str, objectvalues: str, window: Gtk.Window) -> Gtk.Widget:
    configwidget = Gtk.Widget

    if (objecttype == 'entry'):
        configwidget = gtkentry.create_entry(configname)
    elif (objecttype == 'usblist'):
        configwidget = gtkusblist.create_list(configname, window)
    elif (objecttype == 'pcilist'):
        configwidget = gtkpcilist.create_list(configname, window)
    elif (objecttype == 'disklist'):
        configwidget = gtkdisklist.create_list(configname, window)
    elif (objecttype == 'disklistview'):
        configwidget = gtkdisklistview.create_view(configname)
    elif (objecttype == 'bselect'):
        configwidget = gtkswitch.create_state_switch(configname, objectvalues)
    elif (objecttype == 'select'):
        configwidget = gtkselection.create_selection_box(configname, objectvalues)
    elif (objecttype == 'multiselect'):
        configwidget = gtkmultiselection.create_multi_selection_box(configname, objectvalues)
    elif (objecttype == 'check'):
        configwidget = gtkcheckbutton.create_checkbutton_box(configname, objectvalues)
    elif (objecttype == 'numeric'):
        configwidget = gtkspinbutton.create_numeric_spinbutton(configname, objectvalues)

    return configwidget


def get_state_image(configname: str):
    image = Gtk.Image()
    defaultvalue = settings.tlpconfig_defaults[configname].get_value()
    defaultstate = settings.tlpconfig_defaults[configname].is_enabled()
    settings.imagestate[configname] = StateImage(defaultvalue, defaultstate, image)
    settings.tlpconfig[configname].refresh_image_state()
    return image


def get_type_image(configname: str) -> Gtk.Image:
    tlpconfig = settings.tlpconfig[configname]      # type: TlpConfig
    conftype = tlpconfig.get_conf_type()
    conftypeimage = Gtk.Image()

    if conftype == ConfType.DROPIN:
        conftypeimage = Gtk.Image.new_from_file(settings.icondir + 'dropin.svg')
        conftypeimage.set_tooltip_text(tlpconfig.get_conf_path())
    elif conftype == ConfType.USER:
        conftypeimage = Gtk.Image.new_from_file(settings.icondir + 'user.svg')
        conftypeimage.set_tooltip_text(tlpconfig.get_conf_path())

    return conftypeimage


def create_item_box(configobjects, doc, grouptitle, window) -> Gtk.Box:
    configuibox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

    if len(configobjects) > 1:
        transgrouptitle = grouptitle + "__GROUP_TITLE"
        grouplabel = Gtk.Label()
        grouplabel.set_markup(' <b>{}</b> '.format(language.CDT_(transgrouptitle)))
        grouplabel.set_use_markup(True)
        grouplabel.set_margin_bottom(12)
        grouplabel.set_halign(Gtk.Align.START)
        grouplabel.set_valign(Gtk.Align.START)

        configuibox.pack_start(grouplabel, False, False, 0)

    for configobject in configobjects:
        configname = configobject[0]
        configtype = configobject[1]
        possiblevalues = configobject[2]

        tlpuiobject = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)
        tlpuiobject.set_margin_start(18)
        tlpuiobject.set_margin_end(18)

        if configname not in settings.tlpconfig.keys():
            missingcheckbox = Gtk.CheckButton()
            missingcheckbox.set_child_visible(False)
            missingstatetogglebox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            missingstatetogglebox.pack_start(missingcheckbox, False, False, 0)
            missingstatetogglebox.set_halign(Gtk.Align.CENTER)
            missingstatetogglebox.set_valign(Gtk.Align.CENTER)

            missingconfiglabel = Gtk.Label(xalign=0)
            missingconfiglabel.set_name('missingConfigLabel')
            missingconfiglabel.set_markup(' <b>{}</b> - <i>{}</i> '.format(configname, EXPECTED_ITEM_MISSING_TEXT))
            missingconfiglabel.set_use_markup(True)

            tlpuiobject.pack_start(missingstatetogglebox, False, False, 0)
            tlpuiobject.pack_start(missingconfiglabel, False, False, 0)
            configuibox.pack_start(tlpuiobject, True, True, 0)
            continue

        statetogglebox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        tlpconfigbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # on/off state
        toggle = gtktoggle.create_toggle_button(configname, tlpconfigbox)
        statetogglebox.pack_start(toggle, False, False, 0)
        statetogglebox.set_halign(Gtk.Align.CENTER)
        statetogglebox.set_valign(Gtk.Align.CENTER)

        # config state image
        configstateimage = get_state_image(configname)

        # config type image
        configtypeimage = get_type_image(configname)

        # specific config gtk object
        configwidget = create_config_widget(configname, configtype, possiblevalues, window)
        configwidget.set_margin_top(6)
        configwidget.set_margin_bottom(6)
        configwidget.set_margin_left(6)

        # object label
        transconfigtitle = configname + "__ID_TITLE"
        configlabel = Gtk.Label(xalign=0)
        configlabel.set_markup(' <b>{}</b> '.format(language.CDT_(transconfigtitle)))
        configlabel.set_use_markup(True)
        configlabel.set_size_request(300, 0)

        # combine boxes
        tlpconfigbox.pack_start(configlabel, False, False, 0)
        tlpconfigbox.pack_start(configwidget, True, True, 0)

        if configname.endswith('_BAT'):
            image = Gtk.Image.new_from_file(settings.icondir + 'OnBAT.svg')
            tlpconfigbox.pack_start(image, False, False, 12)
        elif configname.endswith('_AC'):
            image = Gtk.Image.new_from_file(settings.icondir + 'OnAC.svg')
            tlpconfigbox.pack_start(image, False, False, 12)

        tlpuiobject.pack_start(statetogglebox, False, False, 0)
        tlpuiobject.pack_start(tlpconfigbox, False, False, 0)
        tlpuiobject.pack_start(configstateimage, False, False, 0)
        tlpuiobject.pack_end(configtypeimage, False, False, 0)

        configuibox.pack_start(tlpuiobject, True, True, 0)

    # object description
    configdescriptionlabel = Gtk.Label()
    configdescriptionlabel.set_markup(doc)
    configdescriptionlabel.set_line_wrap(True)
    configdescriptionlabel.set_margin_top(6)
    configdescriptionlabel.set_margin_bottom(12)
    configdescriptionlabel.set_margin_start(48)
    configdescriptionlabel.set_halign(Gtk.Align.START)
    configdescriptionlabel.set_valign(Gtk.Align.START)

    # horizontal separator
    hseparator = Gtk.HSeparator()

    configuibox.pack_start(configdescriptionlabel, True, True, 0)
    configuibox.pack_start(hseparator, True, True, 0)

    return configuibox


def get_tlp_categories(window, categories) -> OrderedDict:
    propertyobjects = OrderedDict()

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
                    configobjects.append([id, type, values])
            else:
                id = config['id']
                transdescription = id + "__ID_DESCRIPTION"
                type = config['type']
                values = config['values']
                configobjects.append([id, type, values])

            description = language.CDT_(transdescription)

            configbox = create_item_box(configobjects, description, grouptitle, window)
            configbox.set_margin_start(12)
            configbox.set_margin_end(12)
            configbox.set_margin_top(12)
            categorybox.pack_start(configbox, False, False, 0)

        categoryname = category['name']
        transcategory = categoryname + "__CATEGORY_TITLE"
        categorylabel = language.CDT_(transcategory)
        propertyobjects[categoryname] = [categorylabel, categorybox]

    return propertyobjects
