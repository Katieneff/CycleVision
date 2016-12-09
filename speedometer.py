from multiprocessing import Process, Queue, Value
import time, math, threading, RPi.GPIO as GPIO
import sys # debugging

class Speedometer(object):
    """This class defines a Speedometer for a bicycle
        that uses a Hall Effect sensor and a magnet to
        find the revolutions per second of a wheel of
        the bike and computes its speed in miles per
        hour
    """
    def __init__(self, channelNum, wheelDiam):
        super(Speedometer, self).__init__()
        self.DELAY = 0.001
        self.INCHPERSEC_TO_MPH = 90 / 11
        self.speed = Value('d', 0.0)
        self.speed.value = 0.0
        self.channelNum = channelNum
        self.wheelDiam = wheelDiam
        self.wheelCircumference = wheelDiam * math.pi
        self.prevIn = 1
        

        # Configure specified GPIO channel as an input
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channelNum, GPIO.IN)

        # Create monitoring thread to get speed data from sensor
        t = threading.Thread(target=self.monitorSpeedometer)
        t.daemon = True
        t.start()
        self.monitorThread = t


    def getSpeed(self):
        return self.speed.value
        
    def monitorSpeedometer(self):
        self.prevIn = GPIO.input(self.channelNum)
        prevTime = time.time()

        # Poll the speed sensor continually
        while True:
            time.sleep(self.DELAY)
            currentIn = GPIO.input(self.channelNum)
            currentTime = time.time()
            # Detect the magnet passing by
            if (currentIn == 0 and prevIn == 1):
                prevIn = 0
                # Calculate speed in mph using following equation:
                #(Xmph) = (Yrev/s) * (pi*wheelDiam in) / (12in/ft) * (3600s/hr) / (5280ft/mi)
                revsPerSec = 1 / (currentTime - prevTime)
                newSpeed = revsPerSec * self.wheelCircumference / self.INCHPERSEC_TO_MPH
                # Update the speed to the average of the previous speed and the new speed
                self.speed.value = abs(self.speed.value - newSpeed) / 2
                # Update previous time
                prevTime = currentTime

            # Update prevIn once magnet has passed by
            elif (currentIn == 1):
                prevIn = 1

            


