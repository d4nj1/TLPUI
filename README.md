TLPUI - 2021.05.17

The Python scripts in this project generate a GTK-UI to change TLP configuration files easily.
It has the aim to protect users from setting bad configuration and to deliver a basic overview of all the valid configuration values.

Install and run instructions:
* [Python 3](https://github.com/d4nj1/TLPUI/wiki/Install-instructions#python-3)
* [Ubuntu/Debian family](https://github.com/d4nj1/TLPUI/wiki/Install-instructions#ubuntudebian-family)

Current status:

* Supports TLP versions 0.8-1.4(alpha)
* Configuration can be read and displayed
* Shows information about configuration changes (defaults/unsaved and dropin/user config)
* Changes can be saved with user and sudo permissions (e.g. /etc/default/tlp or /etc/tlp.conf)
* tlp-stat can be load in ui (simple and complete)

To be done:

* Translation optimizations - [#79](https://github.com/d4nj1/TLPUI/issues/79)
* PPA - [#88](https://github.com/d4nj1/TLPUI/issues/88)
* Flatpak - [#89](https://github.com/d4nj1/TLPUI/issues/89)
* Implement package build pipeline - [#90](https://github.com/d4nj1/TLPUI/issues/90)


![Screenshot 24.04.2020](https://raw.githubusercontent.com/d4nj1/TLPUI/master/screenshot.png)
