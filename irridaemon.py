#!/usr/bin/env python
 
import sys, time, syslog, ConfigParser, zonethread
from daemon import Daemon
	 
class MyDaemon(Daemon):
	##
	def run(self):
		self.irrigationProcess()
		#while True:
		#	syslog.syslog('looping')
		#	time.sleep(1)
			
			
	def irrigationProcess(self):
		# Load zone data from config file
		zones = self.loadConfig()
		#syslog.syslog("zone dictionary %s"%str(zones))
		
		#load week day
		weekday=time.strftime('%w')
		x= True
		threads = []
		zoneWorking={}
		while x:
			
			while time.localtime(time.time())[5] !=0:
				True
			syslog.syslog("Count Start" % time.localtime(time.time()))
			
			for key in zones:
				days     = zones[key]['days']
				startTime= zones[key]['start']
				duration = int(zones[key]['duration'])
				hhStart  = int(startTime.split('.')[0])
				mmStart  = int(startTime.split('.')[1])

				#Check if this weekday needs irrigation
				#if so check time 
				if weekday in days:
					if time.localtime(time.time())[3] == hhStart and time.localtime(time.time())[4] == mmStart:
					#anif True:
						syslog.syslog("zone add: %s" % key)
						syslog.syslog("duration: %u\n" % duration)
						#if valve has to be open load in array the zone and time to loop for needed time.
						zoneWorking.update({key:duration})
						x= zonethread.zonethread()
						x.setParameters(duration,key,1)
						syslog.syslog("thread start")
						x.start()
						
						
						
						
			# if len(zoneWorking) != 0:
				# for zoneW in zoneWorking.keys():
					# syslog.syslog("ZoneWork: %s" % zoneW)
					# timeLeading=zoneWorking.get(zoneW)
					# #syslog.syslog("ZoneWork: %u" % timeLeading)

					# #at the end of the irrigation cycle zone duration is -1 so close channel and valve
					# if timeLeading == 0:
						# del zoneWorking[zoneW]
						# # Chiudere GPIO
						
					# else:
						# timeLeading=timeLeading-1
						# zoneWorking.update({zoneW:timeLeading})
						# syslog.syslog("timeLeading: %u"%timeLeading)
					
			syslog.syslog("looping")
			time.sleep(1)
				
			
	def loadConfig(self):
		zones={}
		syslog.syslog('loadConfig')
		cfgFileName='/usr/local/share/pi/zones.cfg'
		
		# Load configuration file
		config=ConfigParser.RawConfigParser()
		config.read(cfgFileName)
				
		# Read config Sections
		for zoneKey	in config.sections():
			
			#Split section name to have zone ID
			zoneID=zoneKey.split()[1]
			zoneData={}
			items=config.items(zoneKey)

			# Get Items for each section and create a dictionary from items list
			itemKey = 0
			while itemKey < len(items):
			
				#syslog.syslog('Zone key= %s' % items[itemKey][0])
				#syslog.syslog('Zone item = %s\n' % items[itemKey][1])
				
				zoneData.update({items[itemKey][0]:items[itemKey][1]})
				itemKey = itemKey + 1
				
			zones.update({str(zoneID):zoneData})
		return zones
		
		
		
		
if __name__ == "__main__":
	daemon = MyDaemon('/tmp/irridaemon.pid')
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



	