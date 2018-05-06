import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from shutil import which
from . import language


expecteditemmissing = language.UH_('Expected item missing in config file')  # type: str
sudomissing = language.UH_('Install pkexec, gksu, gksudo, kdesu or kdesudo first.')  # type: str
defaultstatetext = language.UH_('Default state:')  # type: str
defaultvaluetext = language.UH_('Default value:')  # type: str
changedstatetext = language.UH_('CHANGED')  # type: str


def get_graphical_sudo():
    sudo = which("pkexec")
    if sudo is None:
        sudo = which("gksu")
    if sudo is None:
        sudo = which("gksudo")
    if sudo is None:
        sudo = which("kdesu")
    if sudo is None:
        sudo = which("kdesudo")
    return sudo


class StateImage:
    def __init__(self, defaultvalue, defaultstate, stateimage: Gtk.Image):
        self.defaultvalue = str(defaultvalue)
        self.defaultstate = bool(defaultstate)
        self.stateimage = stateimage

    def refresh_image_state(self, value: str, store: str, enabled: bool, enabledstore: bool):
        changed = False
        if enabled != enabledstore or value != store:
            changed = True

        enabledtext = ''
        if enabled != self.defaultstate:
            enabledtext += '{} {}'.format(defaultstatetext, str(self.defaultstate))

        if value == self.defaultvalue:
            if not changed and enabledtext == '':
                self.stateimage.clear()
            elif not changed and enabledtext != '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_INFO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('{}'.format(enabledtext))
            elif changed and enabledtext == '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_UNDO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('{}'.format(changedstatetext))
            elif changed and enabledtext != '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_UNDO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('{}\n{}'.format(changedstatetext, enabledtext))
        else:
            defaulttext = '{} {}'.format(defaultvaluetext, self.defaultvalue)
            if not changed and enabledtext == '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_INFO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text(defaulttext)
            elif not changed and enabledtext != '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_INFO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('{}\n{}'.format(enabledtext, defaulttext))
            elif changed and enabledtext == '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_UNDO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('{}\n{}'.format(changedstatetext, defaulttext))
            elif changed and enabledtext != '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_UNDO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('{}\n{}\n{}'.format(changedstatetext, enabledtext, defaulttext))
