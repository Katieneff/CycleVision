from smbus import SMBus

class Gyroscope(object):
	
	def __init__(self):
		self.bus = SMBus(1)
		# Address of MPU-9150 gyroscope when AD0 port is grounded
		self.addr = 0x68


	def read(self):
		""" Returns Z value of gyroscope"""
		x = self.bus.read_i2c_block_data(self.addr, 0x3B, 4)
		return x[2]
