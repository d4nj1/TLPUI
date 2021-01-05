Flatpak documentation

To build and install the Flatpak in user environment you can call:

`flatpak-builder --force-clean --user --install build-dir org.flatpak.tlpui.json`

To run the Flatpak just execute with:

`flatpak run org.flatpak.tlpui`

Working status:

* Host configuration can be viewed
* Simple tlp-stat output can be fetched

To be done:

* Writing system configuration
* Upload package to Flathub.org
