import BMP085.altimeter as alt
from L3GD20 import gyro
from i2c_adxl345 import i2c_adxl345
from i2c_hmc5883l import i2c_hmc5883l
import numpy as np
import time
import math
class imu:
    def __init__(self):
        self.gyro = gyro.gyro()
        #self.alt = alt()
        self.refGyro = self.getGyroRef()
        #self.refAlt = self.getAltRef()
        self.acc = i2c_adxl345()
        self.mag = i2c_hmc5883l()
	self.refHeading=[0,0,0]
	self.refHeading=self.getHeading()
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
        heading =self.getHeading()
        a=-np.arctan2(raw[1],raw[2])
        b=np.arctan2(raw[0],raw[2])
        #print time.time()-ti
        return np.array((a,b))
    def getAcc(self): # euclidian force vector
        return np.array(self.acc.getAxes())
    def getAccUnit(self): # unit version
        out = np.array(self.acc.getAxes())
        return out/np.linalg.norm(out)
    def getHeading(self):
        out = np.array(self.mag.getAxes())
        out[0] += 0
        out[1] += 100
        out[2] += 60 # Magnet offsets
        return out

lag=50
def kalman():
    X = np.array((1,1,1,1))
    pass

def serveMag(eul):
    while True:
        eul[0],eul[1],eul[2]=i.mag.getAxes()


def wrap(angle):
    return angle
    pi = math.pi
    if angle > pi:
        angle -= (2*pi)
    if angle < -pi:
        angle += (2*pi)
    if angle < 0:
        angle += 2*pi
    return angle
def fixMag(bx,by,bz,pitch,roll):
        Xh = bx*math.cos(pitch) + by*math.sin(roll) * math.sin(pitch) + bz * math.cos(roll) * math.sin(pitch)
        Yh = by * math.cos(roll) - bz*math.sin(roll)
        return wrap(-math.atan2(-Yh,Xh))
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
        heading = i.getHeading()
        #euler = 0.98*(euler + wtdt) + np.append(0.02*(G),0)
        euler = euler + wtdt
        Bx = heading[0]
        By = heading[1]
        Bz = heading[2]
        pitch = euler[0]
        roll = euler[1]
        yaw = euler[2]
        Xh = Bz*math.sin(roll)-By*math.cos(pitch)
        headingC = fixMag(Bx,By,Bz,roll,pitch) # Corrected Heading
        if c == 0:
            if __name__=="__main__":
                #print time.time()-tx
                print euler[0], euler[1], euler[2]
                #print heading
                #print headingC,i.mag.getHeading()
        euler[0] = 0.98*euler[0] + .02*G[0]
        euler[1] = 0.98*euler[1] + .02*G[1] # G's are mixed up...shitty
        euler[2] = headingC
        # Complimentary filter. Easy and effective
        eul[0] = euler[0]
        eul[1] = euler[1]
        eul[2] = euler[2] # Ship some values to the client
def dcm(eul):
    print "starting"
    ti = time.time()
    Rt = np.array((1,0,0,0,1,0,0,0,1)).reshape((3,3)) # initial condition: ground frame = craft frame
    # rzx = Rt[2][0]
    # rzy = Rt[2][1]
    # rzz = Rt[2][2]
    # ryx = Rt[1][0]
    # rxx = Rt[0][0]
    c = 0
    bias = 0
    while True:
        c = (c+1) % lag
        tx = time.time()
        dt = ti - tx
        ti = tx # update timestep
        wt = i.getGyro() # W(t)dt vector
        RP = i.getG()
        wtdt = wt*dt
        Rt = np.dot(Rt,np.array((1,-wtdt[2],wtdt[1],wtdt[2],1,-wtdt[0],-wtdt[1],wtdt[0],1)).reshape((3,3)))
        RPC=np.array([(1,Rt[0][1],RP[0]),
                  (Rt[1][0],1,-RP[1]),
                  (-RP[0],RP[1],1)])
        Rt = 0.98 * Rt + 0.02 * RPC
        x=Rt[0]
        y=Rt[1]
        err=np.dot(x,y)
        f = lambda xo: (1/2.)*(3-np.dot(xo,xo))*xo
        xo = f(x - (err/2)*y)
        yo = f(y - (err/2)*x)
        zo = f(np.cross(xo,yo))
        Rt = np.array((xo,yo,zo))
        if c == 0:
            #The 3 euler angles
            e1 = -math.asin(Rt[2][0])
            e2 = math.atan2(Rt[2][1],Rt[2][2])
            e3 = math.atan2(Rt[1][0],Rt[0][0])
            eul[0] = e1
            eul[1] = e2
            eul[2] = e3
            #f1 = -math.asin(RPC[2][0])
            #f2 = math.atan2(RPC[2][1],RPC[2][2])
            #f3 = math.atan2(RPC[1][0],RPC[0][0])
            #print time.time()-tx,e1,e2,e3
            #print f1,f2,f3
            #print "pitch: {0}\troll: {1}\tyaw: {2}".format(e1,e2,e3),np.linalg.norm(x).__str__()
            #print "pitch: {0}\troll: {1}\t".format(G[0],G[1])
       # f=open("state",mode="w")
       # f.write(x.__str__()+"\n")
       # f.write((ty-tx).__str__())
       # f.close()
i = imu()
#euler= np.array((0,0,0))
#complementary(euler)
if __name__ == "__main__":
    complementary(np.array((0,0,0)) )
    #dcm()
    #while True:
     #   print i.getAcc()
      #  print i.getGyro()
       # time.sleep(.5)
