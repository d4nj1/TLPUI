TLPUI - 06.08.2019

The Python scripts in this projects generate a GTK-UI to change TLP configuration files easily.
It has the aim to protect users from setting bad configuration and to deliver a basic overview of all the valid configuration values.

Preparations:

* TLP installed
* Gtk3 libs installed
* Python3 installed

If you are running a Debian based distribution, you can just run:

```
sudo apt install libcairo2-dev libgirepository1.0-dev
pip install -r requirements.txt
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
