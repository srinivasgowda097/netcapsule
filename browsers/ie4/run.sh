#!/bin/bash
export WINEPREFIX="/home/browser/ie4"

sed -i s/DIMENSION/$SCREEN_WIDTH"x"$SCREEN_HEIGHT/g /home/browser/ie4/user.reg

wine regedit proxy.reg

run_browser wine start /max /W 'C:/Program Files/Internet Explorer/iexplore.exe' $URL

