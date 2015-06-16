import sys
sys.path.append('/var/www/raspberry/service')
from multiprocessing.connection import Client
from array import array
from GardenPi import GardenPi



###########################################################
# Zone Class
# 2013/2014
# Class for a Zone:
# contain all the info for the class 
# 
###########################################################

class Zone:
  
  cfg = GardenPi()
  serverAddress = (cfg.ipaddress,cfg.port)
  authKey=cfg.authkey
  
  zoneid=0
  name=""
  description=""
  imagearea=""
  days=""
  start=""
  duration=""
  started=0
  htmlParameters=dict()
  
  def __init__(self):
    # Setup html parameters to manage config and modify page, used to render the config page
    self.htmlParameters.update({'06_duration':{'desc':'Duration in minutes? ''','type':'n','len':'3'}})
    self.htmlParameters.update({'05_start':{'desc':'Start Time hh.mm 0-24 ','type':'hhmm','len':'5'}})
    self.htmlParameters.update({'04_days':{'desc':'Weekdays (1 Monday, 2 Thuesday... 7 Sunday) ','type':'t','len':'7'}})
    self.htmlParameters.update({'02_description':{'desc':'Zone description: ','type':'t','len':'20'}})
    self.htmlParameters.update({'01_name':{'desc':'Zone Name: ','type':'t','len':'10'}})
    self.htmlParameters.update({'03_imagearea':{'desc':'Image area for this zone.<BR> Point top left xy and Point bottom right xy (x,y,x,y)','type':'t','len':'15'}})
    return 

  def __getattr__(self, attribute):
    return "You asked for %s, but I'm giving you default" % attribute

  def getDefaultFields(self):
  	#Return zone fields
    return ['zoneid','name','description','imagearea','days','start','duration']
 
  def getValue(self,field):
  	#Return value for given field
    return getattr(self,field)

  def startZone(self,duration):
    # start zone sending to Server thread zone id and duration 
    rValue = ""
    try:
      conn = Client(self.serverAddress,authkey=self.authKey)
      conn.send("%s:%s" % (self.zoneid,duration))
      conn.close()
      rValue = "open"
    except:
      rValue = "close"
      #sys.syslog("error opening zone %i" % self.zoneid)
    self.started = 1
    return rValue
	

  def stopZone(self):
    # send duration as -1 to the thread Server to close zone 
    rValue = ""
    try:
      conn = Client(self.serverAddress,authkey=self.authKey)
      conn.send("%s:%s" % (self.zoneid,-1))
      conn.close()
      rValue = "close"
    except:
      rValue = "close"
      sys.syslog("error closing zone %i" % self.zoneid)
    return rValue
	
	
  def isStarted():
    return started 
