import serial
import time


ser = serial.Serial("/dev/ttyUSB0", 115200)
time.sleep(1)


ser.write("h101")
print "101"

time.sleep(5)
print "222"
ser.write("h222")
