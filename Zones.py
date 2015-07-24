from Zone import Zone
import ConfigParser
from multiprocessing.connection import Client
from GardenPi import GardenPi

###########################################################
# Zones Class
# 2013/2014
# Class for Zones management:
# contain a list zones and manager
# read and weite of configuration file
###########################################################

class Zones:
  cfgFileName=""
  zones=[]
  cfg = GardenPi()
	
  def __init__(self):
    #get from parameters the name of the text file for the zone
    self.cfgFileName=self.cfg.zoneCfgFile
    self.zones=[]
    return 
  
  def loadValues(self):
 
    self.zones=[]
    config=ConfigParser.RawConfigParser()
    config.read(self.cfgFileName)
    print self.cfgFileName
    print config.sections()
    for section in config.sections():
      zone = Zone()
      zone.zoneid=config.get(section,"zoneid") 
      zone.name=config.get(section,"name")
      zone.description=config.get(section,"description")
      zone.imagearea=config.get(section,"imagearea")
      zone.imagearea=config.get(section,"imagearea")
      zone.days=config.get(section,"days")
      zone.start=config.get(section,"start")
      zone.duration=config.get(section,"duration")
      #zone.started=config.get(section,"zoneid")
      #fields = zone.getDefaultFields()
      #for value in fields:
      #	exec (("zone.%s=config.get(section,name)") ,value)
      self.zones.append(zone)
    return
	
  def saveConfig2(zones):
    config=ConfigParser.RawConfigParser()
      
    i=0
    while i < len(zones):
      section="Zona %u" % (i+1)
      config.add_section(section )
      for key in zones[i]:
        config.set(section,key,zones[i].get(key))
      i=i+1
      
    with open(cfgFileName,'wb') as configfile:
      config.write(self.configfile)
      
    return
	
  def getAllValuesByName(self,field):
    returnZone=[]
    for zone in self.zones:
       returnZone.append(getattrib(zone,field))
    return returnZone  

  def count(self):
    return len(self.zones)

  def getZones(self):
    return self.zones
	
  def getZoneByID(self,index):
    return self.zones[index]