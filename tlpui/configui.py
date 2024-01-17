"""Create TLP config UI."""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from collections import OrderedDict
from . import settings
from . import language
from .ui_config_objects import gtkswitch, gtkentry, gtkselection, gtkmultiselection, gtkcheckbutton, gtkspinbutton, \
    gtktoggle, gtkusblist, gtkpcilist, gtkdisklist, gtkdisklistview
from .file import ConfType, TlpConfig, get_yaml_schema_object
from .uihelper import get_theme_image, StateImage, EXPECTED_ITEM_MISSING_TEXT


def store_category_num(self, cat, cat_num: int):
    """Store selected config category."""
    settings.userconfig.activecategory = cat_num
    # settings.userconfig.activeposition = self.get_children()[cat_num].get_vadjustment().get_value()
    settings.active_scroll = self.get_children()[cat_num]


def store_scroll_position(self, event):
    """Store current scrolled position."""
    settings.userconfig.activeposition = self.get_vadjustment().get_value()


def create_config_box(window) -> Gtk.Box:
    """Create TLP config box."""
    notebook = Gtk.Notebook()
    notebook.set_name('configNotebook')
    notebook.set_tab_pos(Gtk.PositionType.LEFT)

    tlp_categories = get_tlp_categories(window)
    for name, category_data in tlp_categories.items():
        viewport = Gtk.Viewport()
        viewport.set_name(f'categoryViewport_{name}')
        viewport.add(category_data[1])

        scroll = Gtk.ScrolledWindow()
        scroll.add(viewport)
        scroll.connect("scroll-event", store_scroll_position)

        category_image = get_theme_image(f'tlpui-{name.replace(" ", "-")}-symbolic', Gtk.IconSize.MENU)

        labelbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        labelbox.pack_start(category_image, False, False, 0)
        labelbox.pack_start(category_data[0], True, True, 0)
        labelbox.show_all()

        notebook.append_page(scroll, labelbox)

    notebook.connect('switch-page', store_category_num)

    containerbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    containerbox.pack_start(notebook, True, True, 0)

    activecategory = settings.userconfig.activecategory
    notebook.show_all()
    notebook.set_current_page(activecategory)

    return containerbox


def create_config_widget(configname: str, objecttype: str, objectvalues: str, window: Gtk.Window) -> Gtk.Widget:
    """Create config widget."""
    configwidget = Gtk.Widget

    if objecttype == 'entry':
        configwidget = gtkentry.create_entry(configname)
    elif objecttype == 'usblist':
        configwidget = gtkusblist.create_list(configname, window)
    elif objecttype == 'pcilist':
        configwidget = gtkpcilist.create_list(configname, window)
    elif objecttype == 'disklist':
        configwidget = gtkdisklist.create_list(configname, window)
    elif objecttype == 'disklistview':
        configwidget = gtkdisklistview.create_view(configname)
    elif objecttype == 'bselect':
        configwidget = gtkswitch.create_state_switch(configname, objectvalues)
    elif objecttype == 'select':
        configwidget = gtkselection.create_selection_box(configname, objectvalues)
    elif objecttype == 'multiselect':
        configwidget = gtkmultiselection.create_multi_selection_box(configname, objectvalues)
    elif objecttype == 'check':
        configwidget = gtkcheckbutton.create_checkbutton_box(configname, objectvalues)
    elif objecttype == 'numeric':
        configwidget = gtkspinbutton.create_numeric_spinbutton(configname, objectvalues)

    return configwidget


def init_state_image(configname: str):
    """Create and store state image."""
    image = Gtk.Image()
    defaultvalue = settings.tlpconfig_defaults[configname].get_value()
    defaultstate = settings.tlpconfig_defaults[configname].is_enabled()
    settings.tlpconfig[configname].add_state_image(StateImage(defaultvalue, defaultstate, image))
    return image


def get_type_image(configname: str) -> Gtk.Image:
    """Create config location image."""
    tlpconfig = settings.tlpconfig[configname]      # type: TlpConfig
    conftype = tlpconfig.get_conf_type()
    conftypeimage = Gtk.Image()

    if conftype == ConfType.DROPIN:
        conftypeimage = Gtk.Image.new_from_file(f'{settings.icondir}dropin.svg')
        conftypeimage.set_tooltip_text(tlpconfig.get_conf_path())
    elif conftype == ConfType.USER:
        conftypeimage = Gtk.Image.new_from_file(f'{settings.icondir}user.svg')
        conftypeimage.set_tooltip_text(tlpconfig.get_conf_path())

    return conftypeimage


def create_item_box(configobjects: list, doc: str, grouptitle: str, window) -> Gtk.Box:
    """Create box with config item widgets."""
    configuibox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

    if len(configobjects) > 1:
        grouplabel = Gtk.Label()
        grouplabel.set_markup(f' <b>{grouptitle.replace("_", " ")}</b> ')
        grouplabel.set_use_markup(True)
        grouplabel.set_margin_bottom(12)
        grouplabel.set_halign(Gtk.Align.START)
        grouplabel.set_valign(Gtk.Align.START)

        configuibox.pack_start(grouplabel, False, False, 0)

    for configobject in configobjects:      # type: ConfigObject
        configname = configobject.name
        stateimage = init_state_image(configname)
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
            missingconfiglabel.set_markup(f' <b>{configname}</b> - <i>{EXPECTED_ITEM_MISSING_TEXT}</i> ')
            missingconfiglabel.set_use_markup(True)

            tlpuiobject.pack_start(missingstatetogglebox, False, False, 0)
            tlpuiobject.pack_start(missingconfiglabel, False, False, 0)
            configuibox.pack_start(tlpuiobject, True, True, 0)
            continue

        statetogglebox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        tlpconfigbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # specific config gtk object
        configwidget = create_config_widget(configname, configobject.datatype, configobject.values, window)
        configwidget.set_margin_top(6)
        configwidget.set_margin_bottom(6)
        configwidget.set_margin_left(6)

        # on/off state
        toggle = gtktoggle.create_toggle_button(configname, configwidget, window)
        statetogglebox.pack_start(toggle, False, False, 0)
        statetogglebox.set_halign(Gtk.Align.CENTER)
        statetogglebox.set_valign(Gtk.Align.CENTER)

        # object label
        configlabel = Gtk.Label(xalign=0)
        configlabel.set_markup(f' <b>{configname}</b> ')
        configlabel.set_use_markup(True)
        configlabel.set_size_request(300, 0)

        # combine boxes
        tlpconfigbox.pack_start(configlabel, False, False, 0)
        tlpconfigbox.pack_start(configwidget, True, True, 0)

        if configname.startswith('CPU_SCALING_MIN_FREQ') or configname.startswith('CPU_SCALING_MAX_FREQ'):
            khzlabel = Gtk.Label()
            khzlabel.set_markup('<small>kHz</small>')
            tlpconfigbox.pack_start(khzlabel, False, False, 12)

        if configname.endswith('_BAT'):
            tlpconfigbox.pack_start(Gtk.Image.new_from_file(f'{settings.icondir}OnBAT.svg'), False, False, 12)
        elif configname.endswith('_AC'):
            tlpconfigbox.pack_start(Gtk.Image.new_from_file(f'{settings.icondir}OnAC.svg'), False, False, 12)

        tlpuiobject.pack_start(statetogglebox, False, False, 0)
        tlpuiobject.pack_start(tlpconfigbox, False, False, 0)
        tlpuiobject.pack_start(stateimage, False, False, 0)
        tlpuiobject.pack_end(get_type_image(configname), False, False, 0)

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

    # add description and horizontal separator
    configuibox.pack_start(configdescriptionlabel, True, True, 0)
    configuibox.pack_start(Gtk.HSeparator(), True, True, 0)

    return configuibox


def get_tlp_categories(window) -> OrderedDict:
    """Get categories from TLP schema."""
    propertyobjects = OrderedDict()

    categories = get_yaml_schema_object('categories')
    for category in categories:
        categoryname = category['name']

        # Create category label
        categorylabel = Gtk.Label(language.CDT_(f"{categoryname}__CATEGORY_TITLE"))
        categorylabel.set_alignment(1, 0.5)
        categorylabel.set_margin_top(6)
        categorylabel.set_margin_bottom(6)
        categorylabel.set_margin_left(6)
        categorylabel.set_margin_right(6)

        # Create category box
        categorybox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)

        configs = category['configs']
        for config in configs:
            grouptitle = ""
            configobjects = []

            if 'group' in config:
                grouptitle = config['group']
                transdescription = f"{grouptitle}__GROUP_DESCRIPTION"
                groupitems = config['ids']
                for groupitem in groupitems:
                    configobjects.append(ConfigObject(groupitem['id'], groupitem['type'], groupitem['values']))
            else:
                itemid = config['id']
                transdescription = f"{itemid}__ID_DESCRIPTION"
                configobjects.append(ConfigObject(itemid, config['type'], config['values']))

            configbox = create_item_box(configobjects, language.CDT_(transdescription), grouptitle, window)
            configbox.set_margin_start(12)
            configbox.set_margin_end(12)
            configbox.set_margin_top(12)
            categorybox.pack_start(configbox, False, False, 0)

        propertyobjects[categoryname] = [categorylabel, categorybox]

    return propertyobjects


class ConfigObject:
    """Config object helper class."""

    def __init__(self, name: str, datatype: str, values: str):
        """Init config object helper class parameters."""
        self.name = name
        self.datatype = datatype
        self.values = values
