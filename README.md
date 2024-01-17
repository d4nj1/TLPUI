
<img src="https://raw.githubusercontent.com/d4nj1/TLPUI/master/tlpui/icons/themeable/hicolor/scalable/apps/tlpui.svg" align="left" alt="TLP UI" width="196px">

## TLP UI

The Python scripts in this project generate a GTK-UI to change [TLP](https://github.com/linrunner/TLP) configuration files easily.
It has the aim to protect users from setting bad configuration and to deliver a basic overview of all the valid configuration values.

<img src="https://raw.githubusercontent.com/d4nj1/TLPUI/master/screenshot.png" alt="Screenshot" vspace="20px">

### Install and run instructions :ledger:

<!---* [PyPI](https://github.com/d4nj1/TLPUI/blob/master/docs/INSTALL.md#pypi)-->
* [Poetry](https://github.com/d4nj1/TLPUI/blob/master/docs/INSTALL.md#poetry)
* [Python 3](https://github.com/d4nj1/TLPUI/blob/master/docs/INSTALL.md#python-3)
* [Arch Linux](https://github.com/d4nj1/TLPUI/blob/master/docs/INSTALL.md#arch-linux)

<a href='https://flathub.org/apps/details/com.github.d4nj1.tlpui'><img width='240' alt='Download on Flathub' src='https://flathub.org/assets/badges/flathub-badge-en.png'/></a>

### Current status :sunrise_over_mountains:

* Supports TLP versions 1.3-1.7 - _older TLP versions are supported by [1.6.1](https://github.com/d4nj1/TLPUI/releases/tag/tlpui-1.6.1)_
* Requires Python 3.8 or greater
* Configuration can be read and displayed
* Shows information about configuration changes (defaults/unsaved and drop-in/user config)
* Changes can be saved with user and sudo permissions (/etc/tlp.conf)
* tlp-stat can be load in ui (simple and complete)

### To be done :building_construction:

* Weblate translations - [#121](https://github.com/d4nj1/TLPUI/issues/121)
* Mobile UI - [#111](https://github.com/d4nj1/TLPUI/issues/111)
* Implement package build pipeline - [#90](https://github.com/d4nj1/TLPUI/issues/90)
