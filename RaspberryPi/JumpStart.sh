#!/bin/bash
cd /home/pi/Desktop/Ecotech/RaspberryPi/src
python3 -c 'from networking import network; network.machineUpdate()'
sleep 5
python3 test.py
