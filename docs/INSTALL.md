# Prerequisites

In order to use TLPUI, make sure TLP is installed first

*Debian*
  ```
  sudo apt install tlp tlp-rdw
  sudo tlp start
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

# Ubuntu/Debian family

## Ubuntu PPA with prebuild packages (third party)

These packages are not created by TLPUI author himself, but linuxuprising is a known organisation/website who is also providing many other PPAs.

  ```
  sudo add-apt-repository -y ppa:linuxuprising/apps
  sudo apt update
  sudo apt install tlpui
  ```

## Build and install TLPUI deb package from sources
  
### Install dependencies

  - Ubuntu until 20.10

  ```
  sudo apt install python3-gi git python3-setuptools python3-stdeb python-all dh-python
  ```

  - Ubuntu since 21.04 and Debian bullseye

  ```
  sudo apt install python3-gi git python3-setuptools python3-stdeb dh-python
  ```
  
### Clone TLPUI and build a .deb package
  
  ```
  git clone https://github.com/d4nj1/TLPUI
  cd TLPUI
  python3 setup.py --command-packages=stdeb.command bdist_deb
  sudo dpkg -i deb_dist/python3-tlpui_*all.deb
  ```
  
  - Run TLPUI from the terminal
  
  ```
  tlpui
  ```

# Arch Linux

[tlpui](https://aur.archlinux.org/packages/tlpui/) - Stable release.

[tlpui-git](https://aur.archlinux.org/packages/tlpui-git) - If you always want to use the latest and greatest master branch version from TLPUI repository.
