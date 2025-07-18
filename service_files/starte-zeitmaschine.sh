#!/bin/bash


source /home/zeitmaschine/zeitmaschine/zeitmaschine_project/.venv/bin/activate
python3 /home/zeitmaschine/zeitmaschine/zeitmaschine_project/zeitmaschine/programm.py &



#export DISPLAY=:0

firefox --kiosk "http://127.0.0.1:5000/anzeige"