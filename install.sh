#!/bin/bash

# Filename: install.sh  2016.01.07
# Author: huoty <sudohuoty@163.com>
# Script starts from here:

echo "Install..."
rm -rf ~/.kreminder
mkdir ~/.kreminder
cp -a config icon man kreminder.py systray.py kreminder.sh ~/.kreminder

echo "Creating desktop..."
if [ ! -d "~/.config/autostart" ]
then mkdir -p ~/.config/autostart
fi

rm -rf ~/.config/autostart/kreminder.desktop
echo "[Desktop Entry]" >> ~/.config/autostart/kreminder.desktop
echo "Name=Kreminder" >> ~/.config/autostart/kreminder.desktop
echo "Name[en_IN]=Kreminder" >> ~/.config/autostart/kreminder.desktop
echo "Type=Application" >> ~/.config/autostart/kreminder.desktop
echo "Exec=sh $HOME/.kreminder/kreminder.sh" >> ~/.config/autostart/kreminder.desktop
echo "Hidden=false" >> ~/.config/autostart/kreminder.desktop
echo "NoDisplay=false" >> ~/.config/autostart/kreminder.desktop
echo "X-GNOME-Autostart-enabled=true" >> ~/.config/autostart/kreminder.desktop

echo "Completed!"
exit 0
