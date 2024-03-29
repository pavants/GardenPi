import sys
sys.path.append('/var/www/raspberry')

import time
import calendar
import syslog
import string
import sqlite3 as lite
from multiprocessing.connection import Client
from Zones import Zones
from Zone  import Zone 
from GardenPi import GardenPi
import RPi.GPIO as GPIO




def gotRain(rainSensorPin):
  #SetGPIO pin mode
  GPIO.setmode(GPIO.BOARD)

  #Read Sensor
  GPIO.setup(rainSensorPin,GPIO.IN)
  
  isRaining = GPIO.input(rainSensorPin)
  print (isRaining == 1)
 
  return (isRaining == 1) # if 0 not raining, 1 = is raining



###########################################################
# Watering
# 2014
# Check if it's time to open some valves every minute
###########################################################
syslog.syslog( "watering check running " )

cfg = GardenPi()

rainSensorPin        = cfg.rainPin
rainFlagFile         = cfg.rainFlagFile
waterBudget          = cfg.waterBudget
isRaining            = False
#noWaterTimeAfterRain = cfg.wateringPace * 60 * 60
noWaterTimeAfterRain = 0
#12 * 60 * 60 # 12 hours in seconds
dbName               = cfg.dbName

isRaining = gotRain(rainSensorPin)

# If it is raining exit
if isRaining == True:
  print "it's raining"
  sys.exit(-1)
else:

  #read db to see laast rain time
  conn = lite.connect(cfg.dbName)
  cur = conn.execute("SELECT MAX(rain_time) FROM rain")     
  data = cur.fetchone()
  conn.close()
  print data[0]
  lastRainTuple = time.strptime(data[0],"%Y-%m-%d %H:%M:%S")
  lastRain = calendar.timegm(lastRainTuple)

  #check how many hours past from last rain
  if time.time() - lastRain < noWaterTimeAfterRain: 
    #syslog.syslog( "wait some time. Watering, again at: "+str( time.ctime(lastRain+noWaterTimeAfterRain) ) )
    #Temporary Disable rain check, sensor is broken
    #sys.exit(-1)
    x=1
  syslog.syslog("no rain try irrigation")


######################################
#  chek if it's a day off watering
######################################
#print "Pre test day off"
sqlCmd="SELECT * FROM dayoff WHERE when_stop = '"+time.strftime("%Y%m%d")+"' ;"
#syslog.syslog(sqlCmd)

#print sqlCmd

conn = lite.connect(cfg.dbName)
cur = conn.cursor()
cur.execute(sqlCmd)
row = cur.fetchone()
conn.close()
if  row is not None:
    syslog.syslog("this is a day off raining, exiting")
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
  TIMESEP  = "."
     
  hhStart  = int(startTime.split(TIMESEP)[0])
  mmStart  = int(startTime.split(TIMESEP)[1])

  syslog.syslog("zone %s check day %s, weekday %s, startTime %s, duration %s, hh %s, mm %s" % (zone.zoneid,days, weekday, startTime, duration, hhStart, mmStart))

  # Check if this weekday needs irrigation
  if weekday in days:
    
    # check the clock to see if it is the moment to start  
    syslog.syslog("localtime hh: %i mm: %i - test %i - %i\n" % (time.localtime()[3],time.localtime()[4],hhStart,mmStart))
    if time.localtime()[3] == hhStart and time.localtime()[4] == mmStart:
     
      syslog.syslog("zone start: %s duration: %s\n" % (zone.description,zone.duration))
      syslog.syslog("Count Start %s" % time.strftime("%Y-%m-%d %H:%M:%S"))

      duration = round(int(zone.duration) * waterBudget / 100 )
      
      #Send to server zone and time
      conn = Client(serverAddress,authkey=authKey)
      conn.send("%s:%s" % (zone.zoneid,str(duration)))
      conn.close()
      syslog.syslog("post avvio")
      #zone.startZone(duration)
#return

