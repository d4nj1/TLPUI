#!/usr/bin/env bash
# Download pkg2appimage tool and use it
wget -c $(wget -q https://api.github.com/repos/AppImageCommunity/pkg2appimage/releases -O - | grep "pkg2appimage-.*-x86_64.AppImage" | grep browser_download_url | head -n 1 | cut -d '"' -f 4)
chmod +x ./pkg2appimage-*.AppImage
ARCH=x86_64 ./pkg2appimage-*.AppImage com.github.d4nj1.tlpui.pkg.yml
mv out/TLP_UI-.glibc2.38-x86_64.AppImage out/TLP_UI-x86_64.AppImage
