# P9_19 ---> SCL (L3GD20)
# P9_20 ---> SDA (L3GD20)

import l3gd20
from time import sleep
SMBUS = 1
class gyro:
	def __init__(self,SMBUS=SMBUS,DPS=l3gd20.DPS2000):
		self.bus = l3gd20.setup_bus(SMBUS) 					# bus: 3 indicates /dev/i2c-3
		self.gyro = l3gd20.setup_gyro(self.bus,l3gd20.DPS250)	# gyro scale +/- 2000.0 dps
	def get(self): 
		return l3gd20.get_gyro(self.bus,self.gyro)
if __name__ == "__main__":
        g = gyro()
	
