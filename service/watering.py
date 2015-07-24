import sys
sys.path.append('/var/www/raspberry')

import time
import syslog
import string
from multiprocessing.connection import Client
from Zones import Zones
from Zone  import Zone 
from GardenPi import GardenPi
import RPi.GPIO as GPIO

###########################################################
# Watering  Test
# 2014
# Check if it's time to open some valves every minute
###########################################################

syslog.syslog( "garden daemon running " )

cfg = GardenPi()

sensorPin            = cfg.rainPin
rainFlagFile         = cfg.rainFlagFile
isRaining            = False
noWaterTimeAfterRain = 12 * 60 * 60 # 12 hours in seconds


#SetGPIO ping mode
GPIO.setmode(GPIO.BOARD)

#SetGPIO ping mode
GPIO.setup(sensorPin,GPIO.IN)
isRaining = not GPIO.input(sensorPin)

# If it is raining exit
if not isRaining:
  print "it's raining"
  sys.exit(-1)
else:
  syslog.syslog("check rain")
  #check if it was rain in the last X ours
  lastRain = 0
  try:
    f = open(rainFlagFile,"r")
    lastRain = float(f.read())
    syslog.syslog("lastRain "+str(lastRain))
    f.close()
  except:
    syslog.syslog("norain in last 12 hours let's watering")
    
  #lastRain = 0
  if time.time() - lastRain < noWaterTimeAfterRain: 
    syslog.syslog( "wait some time for watering, again at: "+str( time.ctime(lastRain+noWaterTimeAfterRain) ) )
    sys.exit(-1)

serverAddress = (cfg.ipaddress,cfg.port)
authKey=cfg.authkey

# instantiate zones objects
zones = Zones()
zones.loadValues()

# load week day
weekday=time.strftime('%w')

 
syslog.syslog( "processing irrigation " )
for zone in zones.getZones():
   
  days     = zone.days
  startTime= zone.start
  duration = float(zone.duration) 
  timeSeparator = startTime[2]
     
  hhStart  = int(startTime.split(timeSeparator)[0])
  mmStart  = int(startTime.split(timeSeparator)[1])

  syslog.syslog("zone %s check day %s, weekday %s, startTime %s, duration %s, hh %s, mm %s" % (zone.zoneid,days, weekday, startTime, duration, hhStart, mmStart))

  # Check if this weekday needs irrigation
  if weekday in days:
    
    # if so check the clock to see if it is the moment to start  
    syslog.syslog("localtime hh: %i mm: %i - test %i - %i\n" % (time.localtime()[3],time.localtime()[4],hhStart,mmStart))
    if time.localtime()[3] == hhStart and time.localtime()[4] == mmStart:
     
      syslog.syslog("zone start: %s duration: %s\n" % (zone.description,zone.duration))
      syslog.syslog("Count Start %s" % time.strftime("%Y-%m-%d %H:%M:%S"))
      
      #Send to server zone and time
      conn = Client(serverAddress,authkey=authKey)
      conn.send("%s:%s" % (zone.zoneid,zone.duration))
      conn.close()

