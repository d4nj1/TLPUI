import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


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
            enabledtext += 'Default state: {}'.format(str(self.defaultstate))

        if value == self.defaultvalue:
            if not changed and enabledtext == '':
                self.stateimage.clear()
            elif not changed and enabledtext != '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_INFO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('{}'.format(enabledtext))
            elif changed and enabledtext == '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_UNDO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('CHANGED')
            elif changed and enabledtext != '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_UNDO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('CHANGED\n{}'.format(enabledtext))
        else:
            defaulttext = 'Default value: {}'.format(self.defaultvalue)
            if not changed and enabledtext == '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_INFO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text(defaulttext)
            elif not changed and enabledtext != '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_INFO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('{}\n{}'.format(enabledtext, defaulttext))
            elif changed and enabledtext == '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_UNDO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('CHANGED\n{}'.format(defaulttext))
            elif changed and enabledtext != '':
                self.stateimage.set_from_icon_name(Gtk.STOCK_UNDO, Gtk.IconSize.BUTTON)
                self.stateimage.set_tooltip_text('CHANGED\n{}\n{}'.format(enabledtext, defaulttext))
