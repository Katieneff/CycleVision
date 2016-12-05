import smbus

class Gyroscope:
	
	def __init__(self):
		self.bus = smbus.SMBus(1)
		# Address of MPU-9150 gyroscope when AD0 port is grounded
		self.addr = 0x68


	def read():
		x = self.bus.read_i2c_block_data(self.addr, 0x3B, 4)
		return x[0]
