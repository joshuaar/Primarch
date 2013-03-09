from IMU import i
import itertools as it
import numpy as np
import time

norm = lambda x: x/np.linalg.norm(x)

def Qo(Eq):
    return np.array((
    (Eq,0,0,0),
    (0,Eq,0,0),
    (0,0,Eq,0),
    (0,0,0,Eq)
    ))
Ro = lambda Ea,Eb: np.array((
    (Ea,0,0,0,0,0),
    (0,Ea,0,0,0,0),
    (0,0,Ea,0,0,0),
    (0,0,0,Eb,0,0),
    (0,0,0,0,Eb,0),
    (0,0,0,0,0,Eb)
    ))

#This seems to work
def computeA(p,q,r):
    return np.array((
        (0,-p,-q,-r),
        (p,0,r,-q),
        (q,-r,0,p),
        (r,p,-q,0)
        ))

def computeC(q0,qf):
    dax,day,daz = frame(qf,aref) - frame(q0,aref)
    dbx,dby,dbz = frame(qf,aref) - frame(q0,aref)
    dq= qf-q0
    computeRow = lambda row: row/dq
    return np.array(map(computeRow,(dax,day,daz,dbx,dby,dbz)))
    
    
def computeDCM(q):
    q0,q1,q2,q3 = q
    q0q1,q0q2,q0q3,q1q2,q1q3,q2q3 = map(lambda x:x[0]*x[1],it.combinations(q,2))
    return np.array((
        (1-2*(q2**2 + q3**2),2*(q1q2+q0q3),2*(q1q3-q0q2)),
        (2*(q1q2-q0q3),1-2*(q1**2 + q3**2),2*(q2q3+q0q1)),
        (2*(q1q3+q0q2),2*(q2q3-q0q1),1-2*(q1**2 + q2**2))
        ))
def frame(q,vector):
    return np.dot(computeDCM(q),vector)

def predict(q0,t0):
    global P,Q,R
    p,q,r = i.getGyro()
    meas = getmeas()
    tf = time.time()
    dt = tf-t0
    A = computeA(p,q,r)
    P = np.dot(np.dot(A,P),A.T) + Q # P = APA.T + Q
    xDot = np.dot(A,q0)    
    qf = norm(q0 + xDot * dt)
    return tf, qf, meas, computeC(q0,qf)
def update(qf, meas):
    global P,Q,R,C
    E = np.dot(np.dot(C,P),C.T) + R
    E_ = np.linalg.inv(E)
    K = np.dot(np.dot(P,C.T),E_)
    xe = quat2meas(qf)
    xm = meas
    qf += np.dot(K,(xm-xe))
    P = P - np.dot(np.dot(K,C),P)
    return qf

def getmeas():
    return np.array((norm(i.getAcc()),norm(i.getHeading()))).reshape((6))
def quat2meas(q):
    ax,ay,az = frame(q,aref)
    bx,by,bz = frame(q,bref)
    return np.array((ax,ay,az,bx,by,bz))

#Converts the state q to euler angles
def quat2euler(q):
    gx,gy,gz = frame(q,(0.,0.,1.))
    a=-np.arctan2(gy,gz)
    b=np.arctan2(gx,gz)
    bx,by,bz = frame(q,(1,0,0))
    c = np.arctan2(by,bx)
    return a,b,c
    
count = 0
lag = 10
aref = norm(i.getAcc())
bref = norm(i.getHeading())

q = np.array((1,0,0,0))
C = computeC(q,q)
Q = Qo(0.01)
R = Ro(0.01,0.4) # Ea: ErrAcc Eb: ErrMag
P = np.array((
    (1,1,1,1),
    (1,1,1,1),
    (1,1,1,1),
    (1,1,1,1),
    ))

while True:
    count = (count +1) % lag
    t0 = time.time()
    t0,q, meas, C = predict(q,t0)
    q = update(q, meas)
    if count == 0:
        print quat2euler(q)
        #print "vector:",frame(q,(0,0,1))
