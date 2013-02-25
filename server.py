import IMU as imu
import time
from multiprocessing import Process, Value, Array
euler = Array('d',[0,0,0])
p = Process(target=imu.complementary,args=(euler,))
p.start()
while True:
    cmd = raw_input()
    if cmd == "0":
        p.terminate()
        break
    if cmd == "1":
        for i in euler:
            print i
        
