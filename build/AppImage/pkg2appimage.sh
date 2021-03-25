#!/usr/bin/env bash

# Download app image tool and use
if [ ! -f pkg2appimage-1801-x86_64.AppImage ]; then
    wget https://github.com/AppImage/pkg2appimage/releases/download/continuous/pkg2appimage-1801-x86_64.AppImage
    chmod +x pkg2appimage-1801-x86_64.AppImage
fi
VERSION_EXPANDED=1 ARCH=x86_64 ./pkg2appimage-1801-x86_64.AppImage tlpui.yml
mv out/TLP_UI-.glibc2.32-x86_64.AppImage out/TLP_UI-x86_64.AppImage