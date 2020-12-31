#!/usr/bin/env bash

pkill -f "run.py"

if [ "$1" = "" ] || [ "$1" = "start" ]; then
    echo "process started"
    nohup python3 run.py >> /dev/null &
else
    echo "process stopped"
fi