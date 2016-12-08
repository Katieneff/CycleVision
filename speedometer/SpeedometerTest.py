from Speedometer import Speedometer
from multiprocessing import Process, Queue, Value
import time, math, threading, RPi.GPIO as GPIO

# Create new speedometer using GPIO channel 6 and 25" wheel diameter
speedo = Speedometer(6, 25)

while True:
    time.sleep(1)
    print 'Speed: ' + str(speedo.getSpeed())



