#!/bin/bash

# Set python environment
source /home/pi/.profile
workon env

# I don't know why, but running this program in the only way I can access the Gyroscope
# in python without sudo
PATH_I2CDEVLIB=~/i2cdevlib/
cd ~
sudo timeout 1s ./i2cdevlib/RaspberryPi_bcm2835/MPU6050/examples/MPU6050_example_1

# Have to change permissions of the serial file each time
sudo chmod ug+xr /dev/ttyAMA0

cd /home/pi/CycleVision/motion_tracking/
python headlight_tracking.py
