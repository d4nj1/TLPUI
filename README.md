# TLP UI

<p align="center">
    <img src="https://raw.githubusercontent.com/d4nj1/TLPUI/master/tlpui/icons/themeable/hicolor/scalable/apps/tlpui.svg" alt="TLP UI" width="256">
</p>

The Python scripts in this project generate a GTK-UI to change [TLP](https://github.com/linrunner/TLP) configuration files easily.
It has the aim to protect users from setting bad configuration and to deliver a basic overview of all the valid configuration values.

![Screenshot 2021.02.03](https://raw.githubusercontent.com/d4nj1/TLPUI/master/screenshot.png)

## Install and run instructions

* [Python 3](https://github.com/d4nj1/TLPUI/wiki/Install-instructions#python-3)
* [Ubuntu/Debian family](https://github.com/d4nj1/TLPUI/wiki/Install-instructions#ubuntudebian-family)
* [Arch Linux](https://github.com/d4nj1/TLPUI/wiki/Install-instructions#arch-linux)

## Current status

* Supports TLP versions 0.8-1.5
* Configuration can be read and displayed
* Shows information about configuration changes (defaults/unsaved and dropin/user config)
* Changes can be saved with user and sudo permissions (e.g. /etc/default/tlp or /etc/tlp.conf)
* tlp-stat can be load in ui (simple and complete)

## To be done

* Translation optimizations - [#79](https://github.com/d4nj1/TLPUI/issues/79)
* PPA - [#88](https://github.com/d4nj1/TLPUI/issues/88)
* Flatpak - [#89](https://github.com/d4nj1/TLPUI/issues/89)
* Implement package build pipeline - [#90](https://github.com/d4nj1/TLPUI/issues/90)
