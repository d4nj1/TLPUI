TLPUI - 29.01.2018

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

* Software still in Beta status

What works:

* Configuration can be read and displayed
* Changes can be saved with user permissions
* Must be run with sudo to save system configuration (/etc/default/tlp)
* tlp-stat can be load in ui (simple and complete)

To be done:

* Add debian package build script
* Light/dark themed icons
* Code refactorings


![Screenshot 28.12.2017](https://raw.githubusercontent.com/d4nj1/TLPUI/master/screenshot.png)
