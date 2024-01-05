# Prerequisites

In order to use TLPUI, make sure TLP is installed first

*Debian*
  ```
  sudo apt install tlp tlp-rdw
  ```

*Arch / Manjaro*
  ```
  sudo pacman -S tlp tlp-rdw
  ```

# Poetry

To install and run TLP-UI with it's dependencies locally just execute:

  ```
  poetry install
  poetry run tlpui
  ```

# Python 3

* Download and extract ZIP or pull repository
* Open terminal and go to specific folder
* Type: `python3 -m tlpui`

If you run in to issues when calling TLPUI with `python -m tlpui`, please try to solve by installing the following dependencies.

*Debian*
  ```
  sudo apt install libcairo2-dev libgirepository1.0-dev
  pip install pycairo>=1.18.1 PyGObject>=3.34.0
  ```

*Arch / Manjaro*
  ```
  sudo pacman -S cairo gobject-introspection gtk3
  pip3 install pycairo PyGObject
  ```

# Arch Linux

[tlpui](https://aur.archlinux.org/packages/tlpui/) - Stable release.

[tlpui-git](https://aur.archlinux.org/packages/tlpui-git) - If you always want to use the latest and greatest master branch version from TLPUI repository.
