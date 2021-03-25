#!/usr/bin/env bash
# Create structure and copy files
mkdir TLPUI.AppDir
cp tlpui-appimage.desktop TLPUI.AppDir
cp OnAC.svg TLPUI.AppDir
mkdir -p TLPUI.AppDir/usr/bin
mkdir -p TLPUI.AppDir/usr/lib/python3/dist-packages/
cp -r ../../tlpui TLPUI.AppDir/usr/lib/python3/dist-packages/tlpui/
mkdir -p TLPUI.AppDir/usr/share/metainfo
cp tlpui.appdata.xml TLPUI.AppDir/usr/share/metainfo/tlpui.appdata.xml

# Copy run script
cp AppRun TLPUI.AppDir/usr/bin/tlpui
chmod +x TLPUI.AppDir/usr/bin/tlpui
cp AppRun TLPUI.AppDir/AppRun
chmod +x TLPUI.AppDir/AppRun

# Download app image tool and use
if [ ! -f appimagetool-x86_64.AppImage ]; then
    wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
    chmod +x appimagetool-x86_64.AppImage
fi
ARCH=x86_64 ./appimagetool-x86_64.AppImage TLPUI.AppDir