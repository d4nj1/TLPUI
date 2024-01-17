"""Provide main window parts for TLPUI."""

import importlib
import importlib.metadata
import difflib
import toml

from pathlib import Path
from gi.repository import Gtk, Gdk, GdkPixbuf
from . import settings
from . import language
from .configui import create_config_box
from .file import init_tlp_file_config, create_tmp_tlp_config_file, write_tlp_config, get_changed_properties
from .statui import create_stat_box
from .uihelper import get_flag_image, get_theme_image


def get_app_version() -> str:
    """Get TLP-UI version."""
    try:
        return importlib.metadata.version("tlpui")
    except importlib.metadata.PackageNotFoundError:
        try:
            pyproject = toml.load(Path(__file__).parent.parent / "pyproject.toml")
            return pyproject["tool"]["poetry"]["version"]
        except FileNotFoundError:
            return ""


def reset_scroll_position() -> None:
    """Reset the scroll position."""
    settings.active_scroll.get_vadjustment().set_value(settings.userconfig.activeposition)


def store_window_size(self) -> None:
    """Store current window size in settings."""
    settings.userconfig.windowxsize = self.get_size()[0]
    settings.userconfig.windowysize = self.get_size()[1]


def window_key_events(self, event) -> None:
    """Add window key events like crtl+(q|w|s)."""
    if event.state & Gdk.ModifierType.CONTROL_MASK:
        # close window with ctrl+q or ctrl+w
        if event.keyval in (113, 119):
            quit_tlp_config(None, self)
        # save config with ctrl+s
        if event.keyval == 115:
            save_tlp_config(None, self)


def close_main_window(self, _) -> bool:
    """Close main window."""
    quit_tlp_config(None, self)

    # When delete-event is cancelled we have to return True
    # Otherwise application window will disappear
    return True


def load_tlp_config(_, window: Gtk.Window, reloadtlpconfig: bool) -> None:
    """Load TLP configuration to UI."""
    if reloadtlpconfig:
        init_tlp_file_config()

    new_mainbox = create_main_box(window)
    children = window.get_children()
    for child in children:
        window.remove(child)
    window.add(new_mainbox)
    window.show_all()
    while Gtk.events_pending():
        Gtk.main_iteration()
    reset_scroll_position()


def save_tlp_config(self, window) -> None:
    """Persist TLP configuration changes."""
    changedproperties = get_changed_properties()
    if len(changedproperties) == 0:
        return

    tmpfilename = create_tmp_tlp_config_file(changedproperties)

    saveresponse = changed_items_dialog(
        window,
        tmpfilename,
        language.MT_('Review settings'),
        language.MT_('Save these changes?'))

    if saveresponse == Gtk.ResponseType.OK:
        write_tlp_config(tmpfilename)

        # reload config after file save
        load_tlp_config(self, window, True)


def quit_tlp_config(_, window) -> None:
    """Quit TLPUI and prompt for unsaved changes."""
    settings.userconfig.write_user_config()

    changedproperties = get_changed_properties()
    if len(changedproperties) == 0:
        Gtk.main_quit()
        return

    tmpfilename = create_tmp_tlp_config_file(changedproperties)

    quitresponse = changed_items_dialog(
        window,
        tmpfilename,
        language.MT_('Unsaved settings'),
        language.MT_('Do you really want to quit? No changes will be saved'))

    if quitresponse == Gtk.ResponseType.OK:
        Gtk.main_quit()


def changed_items_dialog(window, tmpfilename: str, dialogtitle: str, message: str) -> Gtk.ResponseType:
    """Dialog to show changed TLP configuration items."""
    dialog = Gtk.Dialog(dialogtitle, window, 0, (
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OK, Gtk.ResponseType.OK
    ))
    dialog.set_default_size(400, 300)

    scrolledwindow = Gtk.ScrolledWindow()
    scrolledwindow.set_hexpand(True)
    scrolledwindow.set_vexpand(True)

    with open(settings.tlpconfigfile, encoding='utf-8') as fromfile:
        fromfilecontent = fromfile.readlines()
    with open(tmpfilename, encoding='utf-8') as tofile:
        tofilecontent = tofile.readlines()
    diff = settings.tlpbaseconfigfile + '\n\n'
    for line in difflib.unified_diff(fromfilecontent, tofilecontent, n=0, lineterm=''):
        if line.startswith('---') or line.startswith('+++'):
            continue
        postfix = '' if line.startswith('-') else '\n'
        diff += line + postfix

    textbuffer = Gtk.TextBuffer()
    textbuffer.set_text(diff)

    textview = Gtk.TextView()
    textview.set_buffer(textbuffer)
    textview.set_editable(False)

    scrolledwindow.add(textview)
    scrolledwindow.set_border_width(12)

    box = dialog.get_content_area()
    box.pack_start(scrolledwindow, True, True, 0)
    box.pack_start(Gtk.Label(f'\n{message}\n'), False, False, 0)

    dialog.show_all()
    response = dialog.run()
    dialog.destroy()

    return response


def create_menu_box(window) -> Gtk.Box:
    """Create application menu from XML structure."""
    xmlmenustructure = """
    <ui>
        <menubar name='menubar'>
            <menu action='FileMenu'>
                <menuitem action='save' />
                <menuitem action='quit' />
            </menu>
            <menu name="language_menu" action='LanguageMenu'>
                <menuitem name="en_EN" action='en_EN' />
                <menuitem name="de_DE" action='de_DE' />
                <menuitem name="es_ES" action='es_ES' />
                <menuitem name="fr_FR" action='fr_FR' />
                <menuitem name="pt_BR" action='pt_BR' />
                <menuitem name="ru_RU" action='ru_RU' />
                <menuitem name="tr_TR" action='tr_TR' />
                <menuitem name="id_ID" action='id_ID' />
                <menu name="zh_CN" action='zhSubMenu'>
                    <menuitem name="zh_CN" action='zh_CN' />
                    <menuitem name="zh_TW" action='zh_TW' />
                </menu>
            </menu>
            <menu name="help_menu" action='HelpMenu'>
                <menuitem name="about_dialog" action='AboutDialog' />
            </menu>
        </menubar>
    </ui>
    """

    uimanager = Gtk.UIManager()
    uimanager.add_ui_from_string(xmlmenustructure)

    actiongroup = Gtk.ActionGroup("actions")
    add_menu_actions(window, actiongroup)
    uimanager.insert_action_group(actiongroup)

    menubar = uimanager.get_widget("/menubar")

    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/en_EN"))
    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/de_DE"))
    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/es_ES"))
    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/fr_FR"))
    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/pt_BR"))
    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/ru_RU"))
    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/tr_TR"))
    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/id_ID"))
    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/zh_CN"))

    menubox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    menubox.pack_start(menubar, False, False, 0)

    return menubox


def repack_language_menuitem(menuitem: Gtk.MenuItem):
    """Repack language menu items for better visibility."""
    menuitemname = menuitem.get_name()
    langimage = get_flag_image(menuitemname)
    langlabel = Gtk.Label(menuitemname.split("_")[0])
    langbox = Gtk.Box()
    langbox.pack_start(langimage, False, False, 12)
    langbox.pack_start(langlabel, False, False, 0)
    [menuitem.remove(child) for child in menuitem.get_children()]
    menuitem.add(langbox)


def create_settings_box(window) -> Gtk.Box:
    """Buttons for direct access in UI."""
    fileentrylabel = Gtk.Label(f"TLP {settings.tlpversion} - {settings.tlpbaseconfigfile}")
    fileentrylabel.set_alignment(0, 0.5)
    reloadbutton = Gtk.Button(label=' ' + language.MT_('Reload'),
                              image=get_theme_image('view-refresh-symbolic', Gtk.IconSize.BUTTON))
    reloadbutton.connect('clicked', load_tlp_config, window, True)
    reloadbutton.set_always_show_image(True)
    savebutton = Gtk.Button(label=' ' + language.MT_('Save'),
                            image=get_theme_image('document-save-symbolic', Gtk.IconSize.BUTTON))
    savebutton.connect('clicked', save_tlp_config, window)
    savebutton.set_always_show_image(True)

    settingsbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    settingsbox.pack_start(fileentrylabel, True, True, 0)
    settingsbox.pack_start(reloadbutton, False, False, 0)
    settingsbox.pack_start(savebutton, False, False, 0)

    return settingsbox


def add_menu_actions(window, actiongroup) -> None:
    """Add actions to application menu."""
    actionfilemenu = Gtk.Action("FileMenu", language.MT_("File"), None, None)
    actiongroup.add_action(actionfilemenu)
    actionfilemenusave = Gtk.Action("save", language.MT_('Save'), None, Gtk.STOCK_SAVE)
    actionfilemenusave.connect("activate", save_tlp_config, window)
    actiongroup.add_action(actionfilemenusave)
    actionfilemenuquit = Gtk.Action("quit", language.MT_('Quit'), None, Gtk.STOCK_QUIT)
    actionfilemenuquit.connect("activate", quit_tlp_config, window)
    actiongroup.add_action(actionfilemenuquit)

    actionlanguagemenu = Gtk.Action("LanguageMenu", language.MT_("Language"), None, None)
    actiongroup.add_action(actionlanguagemenu)

    zhlanguagesubmenu = Gtk.Action("zhSubMenu", "zh", None, None)
    actiongroup.add_action(zhlanguagesubmenu)

    actionhelpmenu = Gtk.Action("HelpMenu", language.MT_("Help"), None, None)
    actiongroup.add_action(actionhelpmenu)

    aboutdialogmenu = Gtk.Action("AboutDialog", language.MT_("About"), None, Gtk.STOCK_INFO)
    actiongroup.add_action(aboutdialogmenu)
    aboutdialogmenu.connect('activate', show_about_dialog)

    langdir = Path(settings.langdir)
    for langobject in langdir.iterdir():
        if langobject.is_dir():
            locale = langobject.name

            if locale == settings.userconfig.language:
                actionlang = Gtk.Action(locale, locale, None, Gtk.STOCK_APPLY)
            else:
                actionlang = Gtk.Action(locale, locale, None, None)

            actionlang.connect("activate", switch_language, locale, window)
            actiongroup.add_action(actionlang)


def show_about_dialog(self):
    """Applications about dialog."""
    aboutdialog = Gtk.AboutDialog()
    aboutdialog.set_title("TLP-UI")
    aboutdialog.set_name("name")
    aboutdialog.set_version(get_app_version())
    aboutdialog.set_comments(language.MT_("UI for TLP written in Python/Gtk"))
    aboutdialog.set_website("https://github.com/d4nj1/TLPUI")
    aboutdialog.set_website_label("TLP-UI @ GitHub")
    aboutdialog.set_authors(["Daniel Christophis"])
    aboutdialog.set_translator_credits("Muhammet Emin AKALAN (05akalan57@gmail.com)")
    aboutdialog.set_license_type(Gtk.License.GPL_2_0)
    aboutdialog.set_logo(GdkPixbuf.Pixbuf.new_from_file_at_size(
        f"{settings.icondir}themeable/hicolor/scalable/apps/tlpui.svg", width=128, height=128)
    )
    aboutdialog.connect('response', lambda dialog, fata: dialog.destroy())
    aboutdialog.show_all()


def switch_language(self, lang: str, window: Gtk.Window) -> None:
    """Language switcher."""
    settings.userconfig.language = lang

    # reload language values
    importlib.reload(language)

    load_tlp_config(self, window, False)


def store_option_num(self, option, option_num: int):
    """Store selected functionality option."""
    settings.userconfig.activeoption = option_num


def create_main_box(window: Gtk.Window) -> Gtk.Box:
    """Create TLP configuration items notebook view."""
    notebook = Gtk.Notebook()
    notebook.set_tab_pos(Gtk.PositionType.TOP)

    menubox = create_menu_box(window)
    settingsbox = create_settings_box(window)
    configbox = create_config_box(window)

    contentbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    contentbox.set_margin_top(18)
    contentbox.set_margin_bottom(18)
    contentbox.set_margin_left(18)
    contentbox.set_margin_right(18)
    contentbox.pack_start(settingsbox, False, False, 0)
    contentbox.pack_start(configbox, True, True, 0)

    configlabel = Gtk.Label(language.MT_('Configuration'))
    configlabel.set_hexpand(True)

    statlabel = Gtk.Label(language.MT_('Statistics'))
    statlabel.set_hexpand(True)

    statbox = create_stat_box()

    notebook.append_page(contentbox, configlabel)
    notebook.append_page(statbox, statlabel)

    mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    mainbox.pack_start(menubox, False, False, 0)
    mainbox.pack_start(notebook, True, True, 0)

    notebook.connect('switch-page', store_option_num)

    activeoption = settings.userconfig.activeoption
    notebook.show_all()
    notebook.set_current_page(activeoption)

    return mainbox
