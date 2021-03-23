#!/usr/bin/env bash
# Create structure and copy files
mkdir TLPUI.AppDir
cp tlpui-appimage.desktop TLPUI.AppDir/tlpui.desktop
cp OnAC.svg TLPUI.AppDir/OnAC.svg
mkdir TLPUI.AppDir/usr/
mkdir TLPUI.AppDir/usr/bin
mkdir TLPUI.AppDir/usr/lib
mkdir TLPUI.AppDir/usr/lib/python3/
mkdir TLPUI.AppDir/usr/lib/python3/dist-packages/
cp -r ../../tlpui TLPUI.AppDir/usr/lib/python3/dist-packages/tlpui/
mkdir TLPUI.AppDir/usr/share
mkdir TLPUI.AppDir/usr/share/metainfo
cp tlpui.appdata.xml TLPUI.AppDir/usr/share/metainfo/tlpui.appdata.xml

#Run script
cp AppRun TLPUI.AppDir/usr/bin/tlpui
chmod +x TLPUI.AppDir/usr/bin/tlpui
cp AppRun TLPUI.AppDir/AppRun
chmod +x TLPUI.AppDir/AppRun

ARCH=x86_64 ./appimagetool-x86_64.AppImage TLPUI.AppDir