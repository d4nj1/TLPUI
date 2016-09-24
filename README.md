TLPUI - 24.09.2016

The Python scripts in this projects generate a GTK-UI to change TLP configuration files easily.
It has the aim to protect users from setting bad configuration and to deliver a basic overview of all the valid configuration values.

Preparations:

* Gtk3 libs installed
* Python3 installed

Start UI:

* Download as ZIP
* Extract ZIP
* Open terminal and go to the extracted files
* Type: `./tlpui.py`

Current status:

* Software works but is still in Beta status

What works:

* Configuration can be read and displayed
* Changes can be saved with user permissions
* Must be run with sudo to save system configuration (/etc/default/tlp)
* tlp-stat can be load in ui

To be done:

* Add/optimize value definitions -> Extract disk configuration for all disks found
* Localization -> Create language po/mo files with library
* Jump to last active tab after reload/save -> Use singleton to store last clicked tab-category (notebook_get_current_page)
* Refactor Python code
* UI improvements for better usability
* Add debian package build script
* Light/dark themed icons


![Screenshot 01.09.2016](https://raw.githubusercontent.com/d4nj1/TLPUI/master/screenshot.png)
