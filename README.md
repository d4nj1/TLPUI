TLPUI - 02.05.2015

The Python scripts in this projects generate a GTK-UI to change TLP configuration files easily.
It has the aim to protect users from setting bad configuration and to deliver a basic overview of all the valid configuration values.

Preparations:

* Gtk3 libs installed
* Python3 installed

Start UI:

* Download as ZIP
* Extract ZIP
* Open terminal and go to the extracted files
* Type: `python3 tlpui.py`

Current status:

* Software works but is still in Beta status

What works:

* Configuration can be read and displayed
* Changes can be saved with user permissions
* Must be run with sudo to save system configuration (/etc/default/tlp)

To be done:

* Get sudo/root permission on demand (e.g. zenity dialog)
* Add/optimize value definitions
* Localization
* Jump to last active tab after reload/save
* Refactor Python code
* UI improvements for better usability
* Add tlp-stat output
* Add debian package build script


![Screenshot 02.05.2015](https://raw.githubusercontent.com/d4nj1/TLPUI/master/screenshot.png)
