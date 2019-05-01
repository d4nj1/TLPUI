TLPUI - 18.03.2019

The Python scripts in this projects generate a GTK-UI to change TLP configuration files easily.
It has the aim to protect users from setting bad configuration and to deliver a basic overview of all the valid configuration values.

Preparations:

* TLP installed
* Gtk3 libs installed
* Python3 installed

- Ubuntu/Debian

  - Install TLP
  
  ```
  sudo apt install tlp tlp-rdw
  sudo tlp start
  ```
  
  - Install dependencies
  
  ```
  sudo apt install python3-gi git python3-setuptools python3-stdeb
  ```
  
  - Clone TLPUI and build a .deb package
  
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


Start UI:

* Download and extract ZIP or pull repository
* Open terminal and go to specific folder
* Type: `python3 -m tlpui`

Current status:

* Software still in Beta status

What works:

* Configuration can be read and displayed
* Shows information about configuration changes (defaults/unsaved)
* Changes can be saved with user and sudo permissions (/etc/default/tlp)
* tlp-stat can be load in ui (simple and complete)

To be done:

* Translation optimizations
* Implement Debian package build pipeline


![Screenshot 28.12.2017](https://raw.githubusercontent.com/d4nj1/TLPUI/master/screenshot.png)
