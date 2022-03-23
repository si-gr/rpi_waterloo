#!/bin/sh
killall 'python /home/pi/workspace/rpi_waterloo/main.py'
python /home/pi/workspace/rpi_waterloo/main.py >> /home/pi/workspace/script.log &