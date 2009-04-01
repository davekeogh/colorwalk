#!/bin/sh

prefix=/usr
version="0.1.0"

echo "Installing Color Walk $version\n"

mkdir -p "$prefix/share/colorwalk"

echo "Copying colorwalk.ui to $prefix/share/colorwalk..."
install colorwalk.ui "$prefix/share/colorwalk/colorwalk.ui"

echo "Copying colorwalk.desktop to $prefix/share/applications..."
install colorwalk.desktop "$prefix/share/applications/colorwalk.desktop"

echo "Copying colorwalk to $prefix/bin ..."
install colorwalk "$prefix/bin/colorwalk"
