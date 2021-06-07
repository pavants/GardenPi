import ConfigParser

###########################################################
# Zone GardenPi
# 2013/2014
# Class for the configuration and general parameters:
# 
###########################################################

class GardenPi:

  #cfgFileName = "/data/gardenpi/service/gardenpi.cfg"
  cfgFileName = "/var/www/raspberry/service/gardenpi.cfg"
  ipaddress   = ""
  port        = 0
  thermoPin   = 0
  rainPin     = 0
  waterBudget = 0
  wateringPace= 0
  authkey     = ""
  zoneCfgFile = ""
  logFilePath = ""
  rainFlagFile= ""
  valvesPin   = ""
  dbName      = ""


  
  def __init__(self):
    section="server"
    config=ConfigParser.RawConfigParser()
    config.read(self.cfgFileName)
    self.ipaddress      = config.get(section,"ipaddress") 
    self.authkey        = config.get(section,"authkey") 
    self.zoneCfgFile    = config.get(section,"zoneCfgFile") 
    self.logFilePath    = config.get(section,"logFilePath") 
    self.logFileHTML    = config.get(section,"logFileHTML") 
    self.valvesPin      = config.get(section,"valvesPin") 
    self.rainFlagFile   = config.get(section,"rainFlagFile")   
    self.waterBudget    = config.getint(section,"waterBudget")   
    self.wateringPace   = config.getint(section,"wateringPace")   
    self.thermoPin      = config.getint(section,"thermoPin") 
    self.rainPin        = config.getint(section,"rainPin") 
    self.port           = config.getint(section,"port") 
    self.dbName         = config.get(section,"dbName") 
