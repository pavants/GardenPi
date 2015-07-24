import time,threading,sys,syslog, RPi.GPIO as GPIO

class zonethread( threading.Thread ) :
	runTime = 0
	zoneID = 0
	pinID = 0
	def run( self ):
		if self.runTime == 0 or self.zoneID == 0 or self.pinID == 0:
			syslog.syslog('received: zone %s on pin %s, time %s ' % ( str(self.zoneID), str(self.pinID), str(self.runTime)))
		else:
			syslog.syslog('opening zone %s on pin %s@%s' % ( str(self.zoneID), str(self.pinID), time.time()))
			time.sleep(self.runTime)
		syslog.syslog("closing zone %s@%s" % (self.zoneID,time.time()))
		sys.exit(0)
		
	def setParameters(self, runTime, zoneID, pinID):
		self.runTime=runTime
		self.zoneID=zoneID 
		self.pinID=pinID
	
	