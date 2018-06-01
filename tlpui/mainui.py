from pathlib import Path

from gi.repository import Gtk, Gdk

import copy
from . import settings
from . import language
from .config import get_changed_properties
from .configui import create_config_box
from .file import read_tlp_file_config, create_tmp_tlp_config_file, write_tlp_config, write_tlp_config_with_sudo
from .statui import create_stat_box
import importlib


def store_windowsize(self):
    settings.windowxsize = self.get_size()[0]
    settings.windowysize = self.get_size()[1]


def window_key_events(self, event):
    if event.state & Gdk.ModifierType.CONTROL_MASK:
        # close window with ctrl+q or ctrl+w
        if event.keyval == 113 or event.keyval == 119:
            quit_tlp_config(None, self)
        # save config with ctrl+s
        if event.keyval == 115:
            save_tlp_config(None, self)


def close_main_window(self, event):
    quit_tlp_config(None, self)

    # When delete-event is canceled we have to return True, otherwise application window will disappear
    return True


def tlp_file_chooser(window):
    filechooser = Gtk.FileChooserDialog(language.MT_('Choose config file'), window, Gtk.FileChooserAction.OPEN, (
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    filechooser.set_local_only(True)

    response = filechooser.run()
    if response == Gtk.ResponseType.OK:
        filepath = filechooser.get_filename()
        settings.tlpconfigfile = filepath
    filechooser.destroy()


def open_file_chooser(self, fileentry, window):
    tlp_file_chooser(window)
    fileentry.set_text(settings.tlpconfigfile)
    load_tlp_config(self, window, True)


def load_tlp_config(self, window: Gtk.Window, reloadtlpconfig: bool):

    if reloadtlpconfig:
        settings.tlpconfig = read_tlp_file_config(settings.tlpconfigfile)
        settings.tlpconfig_original = copy.deepcopy(settings.tlpconfig)

    newmainbox = create_main_box(window)
    children = window.get_children()
    for child in children:
        window.remove(child)
    window.add(newmainbox)
    window.show_all()


def save_tlp_config(self, window):
    changedproperties = get_changed_properties()
    if len(changedproperties) == 0:
        return

    saveresponse = changed_items_dialog(window,
                                    changedproperties,
                                    language.MT_('Review settings'),
                                    language.MT_('Save these changes?'))

    if saveresponse == Gtk.ResponseType.OK:
        tmpfilename = create_tmp_tlp_config_file(changedproperties)

        try:
            write_tlp_config(tmpfilename)
        except PermissionError:
            output = write_tlp_config_with_sudo(tmpfilename)

            if not output == '':
                dialog = Gtk.MessageDialog(window)
                dialog.set_default_size(150, 100)
                dialog.format_secondary_markup(output)
                dialog.run()
                dialog.destroy()
                return

        # reload config after file save
        load_tlp_config(self, window, True)


def quit_tlp_config(self, window):
    settings.persist()

    changedproperties = get_changed_properties()
    if len(changedproperties) == 0:
        Gtk.main_quit()
        return

    quitesresponse = changed_items_dialog(window,
                                    changedproperties,
                                    language.MT_('Unsaved settings'),
                                    language.MT_('Do you really want to quit? No changes will be saved.'))

    if quitesresponse == Gtk.ResponseType.OK:
        Gtk.main_quit()


def changed_items_dialog(window, changedproperties: list, dialogtitle: str, message: str):
    dialog = Gtk.Dialog(dialogtitle, window, 0, (
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OK, Gtk.ResponseType.OK
    ))
    dialog.set_default_size(150, 100)

    currentvaluelabel = Gtk.Label()
    currentvaluelabel.set_markup('<b>{}</b>'.format(language.MT_('Current')))
    newvaluelabel = Gtk.Label()
    newvaluelabel.set_markup('<b>{}</b>'.format(language.MT_('New')))

    changeditems = Gtk.Grid()
    changeditems.set_row_homogeneous(True)
    changeditems.set_column_spacing(12)
    changeditems.attach(Gtk.Label(' '), 0, 0, 1, 2)
    changeditems.attach(currentvaluelabel, 1, 0, 1, 2)
    changeditems.attach(Gtk.Label('>'), 2, 0, 1, 2)
    changeditems.attach(newvaluelabel, 3, 0, 1, 2)
    changeditems.attach(Gtk.Label(' '), 4, 0, 1, 2)

    index = 2
    for property in changedproperties:
        changeditems.attach(Gtk.Label(str(property[0]).rstrip(), halign=Gtk.Align.START), 1, index, 1, 1)
        changeditems.attach(Gtk.Label(property[2], halign=Gtk.Align.START), 3, index, 1, 1)
        index += 1

    box = dialog.get_content_area()
    box.pack_start(Gtk.Label(''), True, True, 0)
    box.pack_start(changeditems, True, True, 0)
    box.pack_start(Gtk.Label('\n{}\n'.format(message)), True, True, 0)

    dialog.show_all()
    response = dialog.run()
    dialog.destroy()

    return response


def create_menu_box(window, fileentry):
    UI_INFO = """
    <ui>
        <menubar name='MenuBar'>
            <menu action='FileMenu'>
                <menuitem action='open' />
                <menuitem action='save' />
                <!--<menuitem action='reload' />-->
                <menuitem action='quit' />
            </menu>
            <menu action='LanguageMenu'>
                <menuitem name="en_EN" action='en_EN' />
                <menuitem name="de_DE" action='de_DE' />
                <menuitem name="ru_RU" action='ru_RU' />
                <menuitem name="id_ID" action='id_ID' />
                <menuitem name="zh_CN" action='zh_CN' />
            </menu>
        </menubar>
    </ui>
    """

    uimanager = Gtk.UIManager()
    uimanager.add_ui_from_string(UI_INFO)

    actiongroup = Gtk.ActionGroup("actions")
    add_menu_actions(window, fileentry, actiongroup)
    uimanager.insert_action_group(actiongroup)

    menubar = uimanager.get_widget("/MenuBar")

    menubox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    menubox.pack_start(menubar, False, False, 0)

    return menubox


def create_settings_box(window, fileentry):
    filebutton = Gtk.Button(label=' ' + language.MT_('Open'), image=Gtk.Image(stock=Gtk.STOCK_OPEN))
    filebutton.connect('clicked', open_file_chooser, fileentry, window)
    reloadbutton = Gtk.Button(label=' ' + language.MT_('Reload'), image=Gtk.Image(stock=Gtk.STOCK_REFRESH))
    reloadbutton.connect('clicked', load_tlp_config, window, True)
    savebutton = Gtk.Button(label=' ' + language.MT_('Save'), image=Gtk.Image(stock=Gtk.STOCK_SAVE))
    savebutton.connect('clicked', save_tlp_config, window)
    quitbutton = Gtk.Button(label=' ' + language.MT_('Quit'), image=Gtk.Image(stock=Gtk.STOCK_QUIT))
    quitbutton.connect('clicked', quit_tlp_config, window)

    settingsbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    settingsbox.pack_start(fileentry, True, True, 0)
    settingsbox.pack_start(reloadbutton, False, False, 0)
    #settingsbox.pack_start(filebutton, False, False, 0)
    #settingsbox.pack_start(savebutton, False, False, 0)
    #settingsbox.pack_start(quitbutton, False, False, 0)

    return settingsbox


def add_menu_actions(window, fileentry, actiongroup):
    actionfilemenu = Gtk.Action("FileMenu", language.MT_("File"), None, None)
    actiongroup.add_action(actionfilemenu)

    actionfilemenuopen = Gtk.Action("open", language.MT_('Open'), None, Gtk.STOCK_OPEN)
    actionfilemenuopen.connect("activate", open_file_chooser, fileentry, window)
    actiongroup.add_action(actionfilemenuopen)
    actionfilemenusave = Gtk.Action("save", language.MT_('Save'), None, Gtk.STOCK_SAVE)
    actionfilemenusave.connect("activate", save_tlp_config, window)
    actiongroup.add_action(actionfilemenusave)
    #actionfilemenureload = Gtk.Action("reload", language.MT_('Reload'), None, Gtk.STOCK_REFRESH)
    #actionfilemenureload.connect("activate", load_tlp_config, window)
    #actiongroup.add_action(actionfilemenureload)
    actionfilemenuquit = Gtk.Action("quit", language.MT_('Quit'), None, Gtk.STOCK_QUIT)
    actionfilemenuquit.connect("activate", quit_tlp_config, window)
    actiongroup.add_action(actionfilemenuquit)

    actionlanguagemenu = Gtk.Action("LanguageMenu", language.MT_("Language"), None, None)
    actiongroup.add_action(actionlanguagemenu)

    langdir = Path(settings.langdir)
    for langobject in langdir.iterdir():
        if langobject.is_dir():
            lang = langobject.name

            if lang == settings.language:
                actionlang = Gtk.Action(lang, lang, None, Gtk.STOCK_APPLY)
            else:
                actionlang = Gtk.Action(lang, lang, None, None)

            actionlang.connect("activate", switch_language, lang, window)
            actiongroup.add_action(actionlang)


def switch_language(self, lang: str, window: Gtk.Window):
    settings.language = lang

    # reload language values
    importlib.reload(language)

    load_tlp_config(self, window, False)


def create_main_box(window: Gtk.Window) -> Gtk.Box:
    notebook = Gtk.Notebook()
    notebook.set_tab_pos(Gtk.PositionType.TOP)

    fileentry = Gtk.Label(settings.tlpconfigfile)
    fileentry.set_alignment(0, 0.5)

    menubox = create_menu_box(window, fileentry)
    settingsbox = create_settings_box(window, fileentry)
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

    return mainbox
