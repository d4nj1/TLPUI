# Prerequisites

## Tlp

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

<a href='https://flathub.org/apps/details/com.github.d4nj1.tlpui'><img width='240' alt='Download on Flathub' src='https://flathub.org/assets/badges/flathub-badge-en.png'/></a>


# Distribution specific packages

## Arch Linux

[tlpui](https://aur.archlinux.org/packages/tlpui/) - Stable release.

[tlpui-git](https://aur.archlinux.org/packages/tlpui-git) - If you always want to use the latest and greatest master branch version from TLPUI repository.


# Run from sources

## Requirements

If you want to run Tlp-ui from sources you have to install Gtk libraries first.

*Debian*
  ```
  sudo apt install libcairo2-dev libgirepository1.0-dev
  ```

*Arch / Manjaro*
  ```
  sudo pacman -S cairo gobject-introspection gtk3
  ```

## Poetry

To install and run TLP-UI with it's dependencies just execute the following from the source folder. Make sure Poetry is
installed on your system.

  ```
  poetry install
  poetry run tlpui
  ```

## Python 3

* Download and extract ZIP or pull repository
* Open terminal and go to specific folder
* Type: `python3 -m tlpui`

If you run in to issues when calling TLPUI with `python -m tlpui`, please try to solve by installing the following dependencies.

*Debian*
  ```
  pip3 install pycairo>=1.25.1 PyGObject>=3.46.0 PyYAML>=6.0.1
  ```

*Arch / Manjaro*
  ```
  pip3 install pycairo PyGObject PyYAML
  ```
