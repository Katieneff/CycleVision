"""
A Bluetooth wrapper class that uses the serial library of python
to communicate with the BlueSMIRF bluetooth module
"""

import serial

class Bluetooth(object):
	
	ser
	
	def __init__(self, devFile, baudrate):
		self.ser = serial.Serial(devFile)
		self.ser.baudrate = baudrate
		
		# Wait for pairing connection
		while True:
			read = self.ser.read(1)
			if read == "C"
			break
		
	
	def write(command)
		ser.write(command)

	
	def close()
		ser.close()
