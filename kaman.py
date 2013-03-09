from IMU import i
import itertools as it
import numpy as np
q = np.array((1,0,0,0))

#if __name__ == "__main__":
    
def computeA():
    p,q,r= i.getGyro()
    return np.array((
        (1,-p,-q,-r),
        (p,1,r,-q),
        (q,-r,1,p),
        (r,p,-q,1)
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
def predict(q):
    n = lambda x: x/np.linalg.norm(x)
    return n(np.dot(computeA(),q))
    
count = 0
lag = 100
while True:
    count = (count +1) % lag
    q = predict(q)
    if count == 0:
        print "vector:",frame(q,(0,0,1))
        print "quats:",q
        print "gyro:",i.getGyro()
