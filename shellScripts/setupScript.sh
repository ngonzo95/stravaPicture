#!/bin/bash
#This script runs before Chromium is launched 
#This script checks for internet connectivity. If there is no connnection
#Open the wifi settings and time zone so the user can change them.

if ping -c 1 asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfadfsadf.com >/dev/null ; then
	echo hi

else
	echo Internet connectivity Confirmed, Doing nothing
fi
