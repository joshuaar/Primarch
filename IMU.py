import BMP085.altimeter as alt
from L3GD20 import gyro
from i2c_adxl345 import i2c_adxl345
import numpy as np
import time
import math
class imu:
    def __init__(self):
        self.gyro = gyro.gyro()
        self.alt = alt()
        self.refGyro = self.getGyroRef()
        self.refAlt = self.getAltRef()
        self.acc = i2c_adxl345()
        self.ri = np.array((0,0,0)) # initial rotation vector pitch roll and yaw
    def getGyro(self):
        return np.array(self.gyro.get()) - self.refGyro
    def getAlt(self):
        return np.array(self.alt.get())  - self.refAlt
    def getGyroRef(self):
        return np.array(self.gyro.get())
    def getAltRef(self):
        return np.array(self.alt.get())
    def getG(self): # returns g angles, unit normalized
        #ti=time.time()
        raw = self.getAcc()
        a=-np.arctan2(raw[1],raw[2])
        b=-np.arctan2(raw[0],raw[2])
        #print time.time()-ti
        return np.array((a,b))
    def getAcc(self): # euclidian force vector
        return np.array(self.acc.getAxes())    

lag=100

def complementary(eul):
    euler = np.array(eul)
    ti = time.time()
    c = 0
    while True:
        c = (c+1) % lag
        tx = time.time()
        dt = ti - tx
        ti = tx # update timestep
        wtdt = i.getGyro()*dt # W(t)dt vector
        G = i.getG()
        #euler = 0.98*(euler + wtdt) + np.append(0.02*(G),0)
        euler = euler + wtdt
        if c == 9:
            eul[0] = euler[0]
            eul[1] = euler[1]
            eul[2] = euler[2] # Ship some values to the client
        euler[0] = 0.98*euler[0] + .02*G[0]
        euler[1] = 0.98*euler[1] + .02*G[1]
        # Complimentary filter. Easy and effective
def dcm():
    print "starting"
    ti = time.time()
    Rt = np.array((1,0,0,0,1,0,0,0,1)).reshape((3,3)) # initial condition: ground frame = craft frame
    # rzx = Rt[2][0]
    # rzy = Rt[2][1]
    # rzz = Rt[2][2]
    # ryx = Rt[1][0]
    # rxx = Rt[0][0]
    c = 0
    while True:
        c = (c+1) % 50
        tx = time.time()
        dt = ti - tx
        ti = tx # update timestep
        wtdt = i.getGyro()*dt # W(t)dt vector
        G=i.getG()
        Rt = np.dot(Rt,np.array((1,-wtdt[2],wtdt[1],wtdt[2],1,-wtdt[0],-wtdt[1],wtdt[0],1)).reshape((3,3)))
        x=Rt[0]
        y=Rt[1]
        err=np.dot(x,y)
        f = lambda xo: (1/2.)*(3-np.dot(xo,xo))*xo
        xo = f(x - (err/2)*y)
        yo = f(y - (err/2)*x)
        zo = f(np.cross(xo,yo))
        Rt = np.array((xo,yo,zo))
        if c == 9:
            #The 3 euler angles
            e1 = -math.asin(Rt[2][0])
            e2 = math.atan2(Rt[2][1],Rt[2][2])
            e3 = math.atan2(Rt[1][0],Rt[0][0])
            print "pitch: {0}\troll: {1}\tyaw: {2}".format(e1,e2,e3),np.linalg.norm(x).__str__()
            print "pitch: {0}\troll: {1}\t".format(G[0],G[1])
            print "."+"\n"*int(math.floor(Rt[0][2]*10)) + "  "*int(math.floor(Rt[0][0]*10)) + "*"
       # f=open("state",mode="w")
       # f.write(x.__str__()+"\n")
       # f.write((ty-tx).__str__())
       # f.close()
i = imu()
#euler= np.array((0,0,0))
#complementary(euler)
if __name__ == "__main__":
    i = imu()
    complementary(np.array((0,0,0)) )
    dcm()
