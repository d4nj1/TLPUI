# Prerequisites

In order to use Tlp-ui, make sure Tlp is installed first.

*Debian*
  ```sh
  sudo apt install tlp tlp-rdw
  ```

*Arch / Manjaro*
  ```shell
  sudo pacman -S tlp tlp-rdw
  ```


# Prepacked runtimes

## PyPI

Tlp-ui is available on [pypi.org](https://pypi.org/project/tlp-ui/) and can simple be installed via.

  ```shell
  pip3 install tlp-ui
  ```

## Flatpak

Instructions on how to install Flatpak version of Tlp-ui can be found [here](https://flathub.org/apps/com.github.d4nj1.tlpui).

## Arch Linux

[tlpui](https://aur.archlinux.org/packages/tlpui/) - Stable release.

[tlpui-git](https://aur.archlinux.org/packages/tlpui-git) - If you always want to use the latest and greatest master branch version from Tlp-ui repository.


# Run from sources

If you want to run Tlp-ui from sources you have to install Gtk libraries first.

*Debian*
  ```shell
  sudo apt install libcairo2-dev libgirepository1.0-dev
  ```

*Arch / Manjaro*
  ```shell
  sudo pacman -S cairo gobject-introspection gtk3
  ```

* Download and extract ZIP or pull repository
* Open terminal and go to project folder

## Poetry

Make sure Poetry is installed on your system then install and run Tlp-ui with it's dependencies.

  ```shell
  poetry install
  poetry run tlpui
  ```

## Python 3

If you want to run Tlp-ui as a Python module just execute

  ```shell
  python3 -m tlpui
  ```

If you run in to issues when calling Tlp-ui like this, please try to solve by installing the following dependencies.

  ```shell
  pip3 install 'PyGObject>=3.46.0' 'PyYAML>=6.0.1' 'toml>=0.10.2'
  ```
