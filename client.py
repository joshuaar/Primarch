import pexpect
import time
child = pexpect.spawn ('ssh pi@192.168.1.118')
child.expect ('.*pass.*: ')
child.sendline ('raspberry' )
child.expect('.*pi@rasp')
child.sendline ('python Primarch/server.py' )
child.expect('.*PRIMARCH.*')
while True:
	ti=time.time()
	child.sendline ('1' )
	child.expect('PRIMARCH')
	x=child.before.split("\r\n")
	pitch,roll,yaw=(float(x[2]),float(x[3]),float(x[4]))
	print "lag(ms):{0}\tpitch:{1}\troll:{2}\tyaw:{3}".format((time.time()-ti)*1000, pitch,roll,yaw)
#child.interact()
