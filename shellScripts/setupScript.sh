#!/bin/bash
#This script runs before Chromium is launched 
#This script checks for internet connectivity. If there is no connnection
#Open the wifi settings and time zone so the user can change them.

i="0"

while [ $i -lt 10 ]
do
	if ping -c 1 google.com >/dev/null ; then
		echo Internet connectivity confirmed. Starting Chromium.
		chromium-browser --noerrdialogs --incognito --kiosk nicholas-gonzalez.com/index0.html
		exit
	fi

	sleep 2
	i=$[$i+1]
done

leafpad /home/pi/Documents/stravaPicture/noInternetText.txt & 
matchbox-keyboard &
sudo raspi-config
sudo leafpad /etc/wpa_supplicant/wpa_supplicant.conf
    sudo reboot

