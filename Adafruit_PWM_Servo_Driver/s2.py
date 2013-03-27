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
def put(ch,percent):
	pwm.setPWM(ch,0,int(servoMin+percent*1.0*(servoMax-servoMin)))                        # Set frequency to 60 Hz
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

while (True):
  # Change speed of continuous servo on channel O
  pwm.setPWM(1, 0, servoMin)
  time.sleep(1)
  pwm.setPWM(1, 0, servoMax)
  time.sleep(1)
  pwm.setPWM(0, 0, servoMin)
  time.sleep(1)
  pwm.setPWM(0, 0, servoMax)
  time.sleep(1)
  put(0,.75)
  put(1,.9)
  time.sleep(1)
  move(0,0,1,0.0003)
  p1=0
  p2=0
  p3=0
  put(0,p1)
  put(1,p2)
  put(2,p3)
  while True:
    wait=0.000007
    pf1=random()
    pf2=random()
    pf3=random()
    pool = multiprocessing.Pool()
    param1 = (0,p1,pf1,wait)
    param2=(1,p2,pf2,wait)
    param3=(2,p3,pf3,wait)
    move(*param1)
    move(*param2)
    move(*param3)
    p1,p2,p3=(pf1,pf2,pf3)

    
   


