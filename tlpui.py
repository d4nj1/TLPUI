#!/usr/bin/env python3

import gi
import argparse
import configparser
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from os import path
from css import get_css_provider
from file import read_tlp_file_config
from mainui import create_main_box, close_window
from lang import available_locales

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--lang', nargs='?', default='', choices=list(available_locales.keys()))

args = parser.parse_args()
lang = available_locales.get(args.lang)

config = configparser.ConfigParser()
config.read('app.ini')
try:
    if lang == '':
        lang = config['locale']['lang']
    elif config['locale']['lang'] == lang:
        pass
    else:
        config['locale']['lang'] = lang
        with open('app.ini', 'w') as configfile:
            config.write(configfile)
except ValueError as e:
    print(e)

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    get_css_provider(),
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

defaultconfigpath = '/etc/default/tlp'

window = Gtk.Window()
window.set_title('TLP-UI')
window.set_default_size(900, 600)

if path.exists(defaultconfigpath):
    tlpconfig = read_tlp_file_config(defaultconfigpath)
    window.add(create_main_box(window, defaultconfigpath, tlpconfig))
else:
    noconfiglabel = Gtk.Label("No config file found at " + defaultconfigpath)
    noconfigbox = Gtk.Box()
    noconfigbox.pack_start(noconfiglabel, True, True, 0)
    window.add(noconfigbox)

window.connect('delete-event', Gtk.main_quit)
window.connect('key-press-event', close_window)
window.show_all()
Gtk.main()
