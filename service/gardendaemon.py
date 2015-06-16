#!/usr/bin/env python
import sys
sys.path.append('/var/www/raspberry')

import time
import syslog
import string
#from zonethread import ZoneThread
from multiprocessing.connection import Client
from daemon import Daemon
from Zones import Zones
from Zone  import Zone 

###########################################################
# Class GardenDaemon
# 2013/2014
# Module for raspberry garden control
# this daemon should start with the system and cycle
# to provide correct openings of the zone valves
# starting a new thread for each zone that has to be opened
###########################################################

class GardenDaemon(Daemon):
  serverAddress = ('10.0.11.20',1909)
  
  
  def run( self ):
    # default method called by start()
    syslog.syslog( "garden daemon running " )
    self.irrigationProcess()
    return
    
  def irrigationProcess(self):
    iterator= True
    # instantiate zones objects
    zones = Zones()
    zones.loadValues()
      
    # Thread List
    threads = []

    syslog.syslog( "processing irrigation " )
      
    # Zone opened
    zoneWorking={}
    while iterator:
      syslog.syslog( "irrigation loop " )
      while time.localtime(time.time())[5] !=0:
        True
        
      # load week day
      weekday=time.strftime('%w')


      #for key in zones:
      for zone in zones.getZones():
        # days     = zones[key]['days']
        # startTime= zones[key]['start']
        # duration = int(zones[key]['duration'])
        # hhStart  = int(startTime.split('.')[0])
        # mmStart  = int(startTime.split('.')[1])
          
        days     = zone.days
        startTime= zone.start
        duration = float(zone.duration)
        timeSeparator = startTime[2]
          
        hhStart  = int(startTime.split(timeSeparator)[0])
        mmStart  = int(startTime.split(timeSeparator)[1])

        syslog.syslog("check day %s, weekday %s, startTime %s, duration %s, hh %s, mm %s" % (days, weekday, startTime, duration, hhStart, mmStart))
      # Check if this weekday needs irrigation
        if weekday in days:
          
          # if so check the clock to see if it is the moment to start  
          if time.localtime(time.time())[3] == hhStart and time.localtime(time.time())[4] == mmStart:
           
            syslog.syslog("zone add: %s" % zone.description)
            syslog.syslog("duration: %s\n" % zone.duration)

            # if valve has to be open load in array the zone and time to loop for needed time.
            zoneWorking.update({zone.zoneid:zone.duration})

            syslog.syslog("Count Start %s" % time.strftime("%Y-%m-%d %H:%M:%S"))
            
            conn = Client(self.serverAddress,authkey='testPwd')
            conn.send("%s:%s" % (zone.zoneid,zone.duration))
            conn.close()
      syslog.syslog("looping")
      time.sleep(1)
    return
    
if __name__ == "__main__":
	daemon = GardenDaemon('/tmp/gardendaemon.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
