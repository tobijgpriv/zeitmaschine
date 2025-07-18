#!/bin/bash
sudo /home/zeitmaschine/zeitmaschine/zeitmaschine_project/linux-router/lnxrouter --ap wlan0 zeitmaschine -p zeitmaschine -g 12 -d &
sleep 10

#Das hier ist eine privesc, der User hat aber sowieso sudo ohne Passwort