# Prerequisites

In order to use Tlp-ui, make sure Tlp is installed first.

*Debian*
  ```
  sudo apt install tlp tlp-rdw
  ```

*Arch / Manjaro*
  ```
  sudo pacman -S tlp tlp-rdw
  ```


# Prepacked runtimes

## Flatpak

Instructions on how to install Flatpak version of Tlp-ui can be found [here](https://flathub.org/apps/com.github.d4nj1.tlpui).


# Distribution specific packages

## Arch Linux

[tlpui](https://aur.archlinux.org/packages/tlpui/) - Stable release.

[tlpui-git](https://aur.archlinux.org/packages/tlpui-git) - If you always want to use the latest and greatest master branch version from Tlp-ui repository.


# Run from sources

If you want to run Tlp-ui from sources you have to install Gtk libraries first.

*Debian*
  ```
  sudo apt install libcairo2-dev libgirepository1.0-dev
  ```

*Arch / Manjaro*
  ```
  sudo pacman -S cairo gobject-introspection gtk3
  ```

* Download and extract ZIP or pull repository
* Open terminal and go to project folder

## Poetry

Make sure Poetry is installed on your system then install and run Tlp-ui with it's dependencies.

  ```
  poetry install
  poetry run tlpui
  ```

## Python 3

If you want to run Tlp-ui as a Python module just execute

  ```
  python3 -m tlpui
  ```

If you run in to issues when calling Tlp-ui like this, please try to solve by installing the following dependencies.

*Debian*
  ```
  pip3 install pycairo>=1.25.1 PyGObject>=3.46.0 PyYAML>=6.0.1
  ```

*Arch / Manjaro*
  ```
  pip3 install pycairo PyGObject PyYAML
  ```
