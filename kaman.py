from IMU import i
import itertools as it
import numpy as np
import time
q = np.array((1,0,0,0))

def computeA(p,q,r):
    return (1./2)*np.array((
        (0,-p,-q,-r),
        (p,0,r,-q),
        (q,-r,0,p),
        (r,p,-q,0)
        ))

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

def predict(qk,t0):
    norm = lambda x: x/np.linalg.norm(x)
    p,q,r = i.getGyro()
    tf = time.time()
    dt = tf-t0
    A = computeA(p,q,r)
    xDot = np.dot(A,qk)
    return tf, norm(qk + xDot * dt)
    
count = 0
lag = 100
while True:
    count = (count +1) % lag
    t0 = time.time()
    t0,q = predict(q,t0)
    if count == 0:
        print q
        print "vector:",frame(q,(0,0,1))
