#!/bin/bash

cp zeitmaschine.service ~/.config/systemd/user
sudo cp lnxrouter.service /etc/systemd/system

chmod +x starte-zeitmaschine.sh
chmod +x starte-lnxrouter.sh

sudo systemctl enable lnxrouter.service

systemctl --user enable zeitmaschine.service