from multiprocessing.connection import Listener
from array import array
from zonethread import ZoneThread
from daemon import Daemon
from GardenPi import GardenPi
import time 
import string
import syslog
import sys 
import logging

###########################################################
# Class Server
# 2013/2014
# Class that wait the commands from the web application
# start a newthread for each zone that has to be opened
###########################################################
#class GardenServer( Thread ):

class GardenServer( Daemon ):
  cfg = GardenPi()
  serverAddress = (cfg.ipaddress,cfg.port)
  authkey    = cfg.authkey
  waterBudget= cfg.waterBudget
  threadList = []
  daemon  = True 


  def run( self ):

    # Cycling reading input from socket
    syslog.syslog("Listener GardenServer Started")
    #listener = Listener(self.address, authkey='testPwd')
    listener = Listener(self.serverAddress,authkey = self.authkey)

    while True:

      # Building listener
      syslog.syslog("waiting for connection")
      conn = listener.accept()

      print 'connection accepted from', listener.last_accepted
      syslog.syslog("connection accepted from ")

      # Receiving message 
      msg = conn.recv()
      
     
      # in case of message "close" cycle exit
      if msg == 'close':
        conn.close()
        listener.close()
        return

      # Control if message is in proper format
      if string.find(msg,":") == -1:
        conn.close()
        listener.close()
        return

      elif len(msg) > 0:  
        # Splitting message
        # message format: zoneId:time
        zoneId   = string.split(msg,":")[0]
        duration = string.split(msg,":")[1]
        
        
        #create thread for the zone
        threadZone = ZoneThread()
        self.threadList.append(threadZone)
        try:
			#set parameters in thread Zone
			threadZone.setParameters(duration,zoneId,1)
			syslog.syslog("opening zone %s for %s @%s" % (zoneId,duration,time.strftime("%Y-%m-%d %H:%M:%S")))
			if duration == - 1:
				threadZone.close()
			else:
				threadZone.start()
        except RuntimeError:  
			syslog.syslog("Error opening zone %s" % (zone ))

    listener.close()
    return
    
  def getThreads( self ):
    return threads

if __name__ == "__main__":
	daemon = GardenServer('/var/tmp/gardenserver.pid')
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
