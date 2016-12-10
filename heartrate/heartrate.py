from multiprocessing import Process, Queue, Value
from collections import deque
import time, math, threading, RPi.GPIO as GPIO
import spi

class Heartrate(object):
    """This class defines a Heartrate monitor for a bicycle
        that uses a photodiode to measure the light passing
        through the rider's finger to find their pulse.
    """
    def __init__(self):
        super(Heartrate, self).__init__()
        # short delay for once a hearbeat has been detected
        self.SHORT_DELAY = 0.0001
        # long delay for between heartbeats
        self.LONG_DELAY = 0.004
        self.NUM_READINGS = 10
        self.heartrate = Value('d', 0.0)
        self.heartrate.value = 0.0
        self.measurements = deque([0], self.NUM_READINGS)
        

        # Open SPI device 0
        self.spi = spi.SPI("/dev/spidev0.0")

        # Create monitoring thread to get heartrate data from sensor
        t = threading.Thread(target=self.monitorHeartrate)
        t.daemon = True
        t.start()
        self.monitorThread = t


    def getHeartrate(self):
        # 4 is a fudge factor; sensor triggers multiple times per beat
        return self.heartrate.value / 4
        
    def monitorHeartrate(self):
        delay = self.SHORT_DELAY
        cutoffMSD = 6
        cutoffLSD = 10
        prevIn = [0, 255, 255]
        prevTime = 0
        currentTime = 0
        # Poll the heartrate sensor continually
        while True:
            time.sleep(delay)
            currentIn = self.spi.transfer([0x1, 0x8, 0x0])
            print currentIn
            # Detect start of heartbeat
            if (currentIn[1] == 0 and currentIn[2] < cutoffLSD
                and prevIn[1] > cutoffMSD):
                startTime = time.time()
                prevIn = currentIn
                delay = self.SHORT_DELAY
            # Detect end of heartbeat
            elif (currentIn[1] > cutoffMSD
                  and prevIn[1] == 0 and prevIn[2] < cutoffLSD):
                endTime = time.time()
                prevIn = currentIn
                delay = self.LONG_DELAY
                # Compute BPM
                self.measurements.append(60 / (endTime-startTime))
                # Set new heartrate only after min number of readings have been taken
                if (len(self.measurements) == self.NUM_READINGS):
                    self.heartrate.value = self.queueAverage()
            
    def queueAverage(self):
        average = 0
        for rate in self.measurements:
            average += rate
        return average / len(self.measurements)
