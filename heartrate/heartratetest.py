from heartrate import Heartrate
import time

hr = Heartrate()

while True:
    time.sleep(1)
    print 'Heartrate: ' + str(hr.getHeartrate())
