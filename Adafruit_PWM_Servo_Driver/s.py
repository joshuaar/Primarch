#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
from random import random
# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 20                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)
#def put(ch,percent):
#	pwm.setPWM(ch,0,int(servoMin+percent*1.0*(servoMax-servoMin)))                        # Set frequency to 60 Hz
#	return percent
def put(ch,percent):
	if percent > 1:
		percent = 1
	elif percent < 0:
		percent = 0
        pwm.setPWM(ch,0,int(servoMin+percent*1.0*(servoMax-servoMin)))                        # Set frequency to 60 Hz
        return percent
def putRand(ch):
	put(ch,random())
import multiprocessing
def move(ch,p0,pf,sleep=0.1): # p0 is initial position, pf is final
	put(ch,p0)
	p=p0
	T=4000
	dp = (pf - p0)*T
	while p < pf:
		p+=1.0/T
		put(ch,p)
		time.sleep(sleep)
	while p > pf:
		p-=1.0/T
		put(ch,p)
		time.sleep(sleep)
	put(ch,pf)

def multiput(chs,p):
	chp = zip(chs,p)
	for i in chp:
		put(*i)

chs = [0,1]
#p0 = [1,0]
#pf = [0,1]
#speed = 1
#nSteps = 360
mp = lambda p: multiput(chs,p)
getdir = lambda p0,pf: [-1 if i0-iF > 0 else 1 for i0,iF in zip(p0,pf)]
getcont=lambda p,pf,dir: [p[i]*dir[i]<pf[i]*dir[i]  for i in range(len(dir))]
pnext = lambda p,cont,dir,stepDist: [(p[i]+dir[i]*stepDist) if cont[i] else p[i] for i in range(len(dir))]
#p = p0
def multimove(chs,p0,pf,speed=1, nSteps = 360,putP0=True):
	mp = lambda p: multiput(chs,p) # curry the put function
	dir = getdir(p0,pf)
	stepDist = 1.0/nSteps
	pn = lambda p,cont: pnext(p,cont,dir,stepDist) # curry the pnext function
	gc = lambda p: getcont(p,pf,dir)
        if putP0:
                mp(p0)
        waitFactor = -speed + 1
	p = p0
	cont = gc(p)
	while max(cont):
		p = pn(p,cont)
		mp(p)
		time.sleep(waitFactor)
		cont = gc(p)


def randomScan(nSteps=300,speed=1):
	p0=[0,0]
	while True:
		pf=[random(),random()]
		multimove(chs,p0,pf,nSteps=nSteps,speed=speed)
		p0=pf

    
   


