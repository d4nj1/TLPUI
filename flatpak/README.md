## Flatpak documentation

Until TLPUI flatpak will be released on https://flathub.org you have to build it yourself. Please follow the steps below:

1. Make sure you have runtime and SDK installed like this:

  `flatpak install flathub org.gnome.Platform//3.38 org.gnome.Sdk//3.38`

2. To build and install the Flatpak in user environment you can call from inside the **flatpak** folder:

  `flatpak-builder --force-clean --user --install build-dir com.github.d4nj1.tlpui.json`

3. To run the Flatpak execute:

  `flatpak run com.github.d4nj1.tlpui`
