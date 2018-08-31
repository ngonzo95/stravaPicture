#!/bin/bash
#This script runs after chromium is started on the raspberry pi.
#This  script pulls from github, ensures all requirements are installed
#and then runs run.py indefinetly
cd ~/Documents/stravaPicture
git pull >> picLog.txt || true
pip install -r requirements.txt >> picLog.txt


