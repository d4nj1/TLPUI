TLPUI README - 02.05.2015

The Python scripts in this projects generate a GTK-UI to change TLP configuration files easily.
It has the aim to protect user from entering bad data and to deliver a basic overview of all the valid configuration values.

Preparations:

* Gtk3 libs installed
* Python3 installed

Current status:

* Software works but is still in Beta status

What works:

* Configuration can be read without any problem
* Changes can be saved with user permissions
* Must be run with sudo to save default configuration in /etc/default/tlp

To be done:

* Get sudo/root permission on demand (e.g. zenity dialog)
* Add/optimize value definitions
* Localization
* Jump to latest position after reload/save
* Refactor python code
* UI improvements for better usability
* Add tlp-stat output

![Screenshot 02.05.2015](https://raw.githubusercontent.com/d4nj1/TLPUI/master/screenshot.png)
