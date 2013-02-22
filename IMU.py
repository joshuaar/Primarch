import BMP085.altimeter as alt
import L3GD20.gyro as gyro

class imu:
    def __init__(self):
        self.gyro = gyro()
        self.alt = alt()
