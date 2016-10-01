import gettext

from gi.repository import Gtk, Gdk

from config import get_changed_properties
from configui import create_config_box
from file import read_tlp_file_config, write_tlp_file_config
from statui import create_stat_box

trans = gettext.translation('mainui', 'lang/', languages=['de_DE', 'en_EN'])
T_ = trans.gettext

def close_window(self, event):
    # ctrl+q or ctrl+w
    if event.state & Gdk.ModifierType.CONTROL_MASK and (event.keyval == 113 or event.keyval == 119):
        if self.get_name() == 'GtkWindow':
            Gtk.main_quit()
        else:
            self.destroy()


def open_file_chooser(self, fileentry, window):
    filechooser = Gtk.FileChooserDialog(T_('Choose config file'), None, Gtk.FileChooserAction.OPEN, (
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    filechooser.set_local_only(True)

    response = filechooser.run()
    if response == Gtk.ResponseType.OK:
        filepath = filechooser.get_filename()
        fileentry.set_text(filepath)
    filechooser.destroy()

    load_tlp_config(self, fileentry.get_text, window)


def load_tlp_config(self, filenamepointer, window):
    filename = filenamepointer()
    tlpconfig = read_tlp_file_config(filename)

    newmainbox = create_main_box(window, filename, tlpconfig)
    children = window.get_children()
    for child in children:
        window.remove(child)
    window.add(newmainbox)
    window.show_all()


def save_tlp_config(self, filenamepointer, tlpconfig, window):
    changedproperties = get_changed_properties(tlpconfig)

    dialog = Gtk.MessageDialog()
    dialog.set_default_size(150, 100)
    dialog.connect('key-press-event', close_window)

    if len(changedproperties) == 0:
        dialog.format_secondary_markup('<b>' + T_('No changes') + '</b>')
    else:
        infotext = '<b>' + T_('Changed values:') + '</b>\n'
        for property in changedproperties:
            infotext += '<small>' + property[0] + ' -> ' + property[2] + '</small>\n'

        dialog.format_secondary_markup(infotext.rstrip())
        filename = filenamepointer()
        try:
            write_tlp_file_config(changedproperties, filename)
            # reload config after file save
            load_tlp_config(self, filenamepointer, window)
        except PermissionError as error:
            dialog.format_secondary_markup(repr(error))

    dialog.run()
    dialog.destroy()


def quit_tlp_config(self, tlpconfig, window):
    changedproperties = get_changed_properties(tlpconfig)
    if len(changedproperties) == 0:
        Gtk.main_quit()
        return

    dialog = Gtk.Dialog(T_('Confirm quit'), window, 0, (
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OK, Gtk.ResponseType.OK
    ))
    dialog.set_default_size(150, 100)

    changeditemstext = T_('Do you really want to quit?\nFollowing items have changed:') + '\n\n'
    for property in changedproperties:
        changeditemstext += (property[0] + " -> " + property[2] + "\n\n")
    changeditemstext += T_('No changes will be saved.')

    label = Gtk.Label(changeditemstext)
    label.set_valign(Gtk.Align.CENTER)
    box = dialog.get_content_area()
    box.pack_start(label, True, True, 0)

    dialog.show_all()
    response = dialog.run()

    if response == Gtk.ResponseType.OK:
        Gtk.main_quit()

    dialog.destroy()


def create_settings_box(window, configpath, tlp_config_items):
    fileentry = Gtk.Label(configpath)
    fileentry.set_alignment(0, 0.5)

    filebutton = Gtk.Button(label=' ' + T_('Open'), image=Gtk.Image(stock=Gtk.STOCK_OPEN))
    filebutton.connect('clicked', open_file_chooser, fileentry, window)

    reloadbutton = Gtk.Button(label=' ' +T_('Reload'), image=Gtk.Image(stock=Gtk.STOCK_REFRESH))
    reloadbutton.connect('clicked', load_tlp_config, fileentry.get_text, window)
    savebutton = Gtk.Button(label=' ' + T_('Save'), image=Gtk.Image(stock=Gtk.STOCK_SAVE))
    savebutton.connect('clicked', save_tlp_config, fileentry.get_text, tlp_config_items, window)
    quitbutton = Gtk.Button(label=' ' + T_('Quit'), image=Gtk.Image(stock=Gtk.STOCK_QUIT))
    quitbutton.connect('clicked', quit_tlp_config, tlp_config_items, window)

    settingsbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    settingsbox.pack_start(fileentry, True, True, 0)
    settingsbox.pack_start(reloadbutton, False, False, 0)
    settingsbox.pack_start(filebutton, False, False, 0)
    settingsbox.pack_start(savebutton, False, False, 0)
    settingsbox.pack_start(quitbutton, False, False, 0)

    return settingsbox


def create_main_box(window, configpath, tlp_config_items) -> Gtk.Box:
    notebook = Gtk.Notebook()
    notebook.set_tab_pos(Gtk.PositionType.TOP)

    settingsbox = create_settings_box(window, configpath, tlp_config_items)
    configbox = create_config_box(tlp_config_items)

    contentbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    contentbox.set_margin_top(18)
    contentbox.set_margin_bottom(18)
    contentbox.set_margin_left(18)
    contentbox.set_margin_right(18)
    contentbox.pack_start(settingsbox, False, False, 0)
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
