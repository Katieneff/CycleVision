#!/bin/bash

export PYTHONPATH=/home/pi/opencv-2.4.10:$PYTHONPATH

source ~/.profile
workon env

# Change permissions of serial device file (bluetooth)
sudo chmod ug+rw /dev/ttyAMA0

