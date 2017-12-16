#!/bin/bash
#This script runs before Chromium is launched 
#This script checks for internet connectivity. If there is no connnection
#Open the wifi settings and time zone so the user can change them.

if ping -c 1 asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfadfsadf.com >/dev/null ; then
	echo Internet connectivity confirmed. Do nothing.

else
	leafpad /home/pi/Documents/stravaPicture/noInternetText.txt & 
	matchbox-keyboard &
	sudo raspi-config
	sudo leafpad /etc/wpa_supplicant/wpa_supplicant.conf
fi
