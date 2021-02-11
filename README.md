TLPUI - 2021.02.11

The Python scripts in this project generate a GTK-UI to change TLP configuration files easily.
It has the aim to protect users from setting bad configuration and to deliver a basic overview of all the valid configuration values.

Install and run instructions:
* [Python 3](https://github.com/d4nj1/TLPUI/wiki/Install-instructions#python-3)
* [Ubuntu/Debian family](https://github.com/d4nj1/TLPUI/wiki/Install-instructions#ubuntudebian-family)

Current status:

* Software still in Beta status
* Supports TLP versions 0.8-1.3

What works:

* Configuration can be read and displayed
* Shows information about configuration changes (defaults/unsaved and dropin/user config)
* Changes can be saved with user and sudo permissions (e.g. /etc/default/tlp or /etc/tlp.conf)
* tlp-stat can be load in ui (simple and complete)

To be done:

* Translation optimizations
* Improve/enhance test environment
* Codestyle and docstyle refactorings
* Implement Debian package build pipeline
* Provide distribution independent package (Flatpak see [#31](https://github.com/d4nj1/TLPUI/issues/31))


![Screenshot 24.04.2020](https://raw.githubusercontent.com/d4nj1/TLPUI/master/screenshot.png)
