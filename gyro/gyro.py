import smbus

bus = smbus.SMBus(1)

# Address of MPU-9150 gyroscope when AD0 port is grounded                         
addr = 0x68

while True:
	try:
		# Read x-plane value from accelerometer
		x = bus.read_i2c_block_data(addr, 0x3B, 4)
		# Prints unsigned byte value of reading
		print x[0]
		
	except:
		print 'exiting...'
		break
