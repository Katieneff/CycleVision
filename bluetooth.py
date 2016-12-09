import serial

class Bluetooth(object):
	"""
	A Bluetooth wrapper class that uses the serial library of python
	to communicate with the BlueSMIRF bluetooth module
	"""

	def __init__(self, devFile, baud):
		self.ser = serial.Serial(port=devFile,
                                         baudrate=baud)
		
		# Wait for pairing connection
	#	while True:
	#		read = self.ser.read(1)
			#if read == "C":
			#	break
		
	
	def write(self, command):
                try:
                        self.ser.write(command)
                except serial.serialutil.SerialException:
                        print "Write failed. Continuing."
	
	def close(self):
		self.ser.close()
