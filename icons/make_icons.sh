#!/usr/bin/env bash
# convert png (512x512) -> icns (MacOSX app icon) & ico (Windows app icon)
# you need imagemagick (convert)
# > brew install imagemagick
# iconutil is MacOSX original command
if [ $(uname -s) != "Darwin" ]; then
    echo "You can run this script only on the Mac OSX"
    exit 1
fi
if [ $# != 1 ]; then
    echo "Usage: make_icons.sh [name]"
    exit 1
fi
name=$1
org="${name}.png"
if [ ! -f ${org} ]; then
    echo "${org} not found"
    exit 1
fi
isdir="${name}.iconset"
if [ -e {isdir} ]; then
    rm -rf ${isdir}
fi
mkdir ${isdir}
convert -resize 16x16! ${org} ${isdir}/icon_16x16.png
convert -resize 32x32! ${org} ${isdir}/icon_16x16@2x.png
convert -resize 32x32! ${org} ${isdir}/icon_32x32.png
convert -resize 64x64! ${org} ${isdir}/icon_32x32@2x.png
convert -resize 64x64! ${org} ${isdir}/icon_64x64.png
convert -resize 128x128! ${org} ${isdir}/icon_64x64@2x.png
convert -resize 128x128! ${org} ${isdir}/icon_128x128.png
convert -resize 256x256! ${org} ${isdir}/icon_128x128@2x.png
convert -resize 256x256! ${org} ${isdir}/icon_256x256.png
convert -resize 512x512! ${org} ${isdir}/icon_256x256@2x.png
convert -resize 512x512! ${org} ${isdir}/icon_512x512.png
iconutil -c icns ${isdir} -o ${name}.icns
rm -rf ${isdir}
convert ${org} -define icon:auto-resize ${name}.ico
