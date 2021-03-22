#!/usr/bin/env bash
mkdir TLPUI.AppDir
cp tlpui-package.desktop TLPUI.AppDir/tlpui.desktop
mkdir TLPUI.AppDir/usr/
mkdir TLPUI.AppDir/usr/bin
mkdir TLPUI.AppDir/usr/lib
mkdir TLPUI.AppDir/usr/lib/python3/
mkdir TLPUI.AppDir/usr/lib/python3/dist-packages/
cp -r ../../tlpui TLPUI.AppDir/usr/lib/python3/dist-packages/tlpui/

cp AppRun TLPUI.AppDir/usr/bin/tlpui
chmod +x TLPUI.AppDir/usr/bin/tlpui
cp AppRun TLPUI.AppDir/AppRun
chmod +x TLPUI.AppDir/AppRun


ARCH=x86_64 ./appimagetool-x86_64.AppImage TLPUI.AppDir