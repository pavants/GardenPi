import time
import threading
import sys
import syslog
import RPi.GPIO as GPIO
import sqlite3 as lite
from GardenPi import GardenPi

###########################################################
# Class zonethread
# 2013/2014
# Class that manage the zone opening 
# this class has to be called to open a zone  
###########################################################

class ZoneThread( threading.Thread ):
  duration = 0
  zoneID = 0
  cfg = GardenPi()
  GPIOPin = cfg.valvesPin.split(",")

  logFilePath = cfg.logFilePath
  logFileHTML = cfg.logFileHTML
  dbName      = cfg.dbName

  def __init__(self):
    #Call super constructor
    super(ZoneThread, self).__init__()
    
    return
  
  def run(self):
    #Running method
    boardPin = 0
    
    # check if zone id received is compatible with number of zones
    if self.zoneID-1 > len(self.GPIOPin) or self.zoneID-1 <0: 
      print "zone id received wrong"
      sys.exit(0)
    


    #load the gpio pin from the parameters 
    #(-1 to pair array value with zone value, 
    #    array start from 0 zone start from 1
    boardPin = self.GPIOPin[self.zoneID-1]

    if self.duration == 0 or self.zoneID == 0 or self.duration > 100 or self.zoneID > 4 or boardPin == 0:
      syslog.syslog('ERROR: received: zone %s duration %s ' % ( str(self.zoneID), str(self.duration)))
      return
    
    
    # Opening Pin on BOARD
    # Using pin numeration referring to board pin number 
    #
    #
    #  Raspberry GPIO board pin layout
    #  ________________________________ Raspberry Board border
    #      2 4 6 8 1 2 4 6 8 0 2 4 6
    #              0 1 1 1 1 2 2 2 2
    #  |   . . . . . . . . . . . . .
    #  |   . . . . . . . . . . . . .
    #      1 3 5 7 9 1 3 5 7 9 1 3 5
    #                1 1 1 1 1 2 2 2
    #
    if True:
      mx = []
      #Write event in Logger
      mx = ["start",str(self.zoneID), str(boardPin), time.strftime("%H:%M:%S")]
      print mx[1]
      self.writeLog(mx)
      
      # Open requested pin on raspy board
      # setting GPIO mode
      GPIO.setmode(GPIO.BOARD)  
      #Disable warning if already open
      GPIO.setwarnings(False)
      # setting out  
      GPIO.setup(int(boardPin), GPIO.OUT)

      # turning on voltage
      GPIO.output(int(boardPin), GPIO.HIGH)

      ##### Update database
      con = lite.connect(self.dbName)
      cur = con.cursor()      
      #insert start event
      cur.execute("INSERT INTO events (event,zone_id) VALUES('start',"+str(self.zoneID)+")")
      cur.execute("SELECT last_insert_rowid()")
      row=cur.fetchone()
      con.commit()
      
	
      #get row id
      transactionID=row[0]
      print transactionID
      
      # Sleeping for the time requested 
      #time.sleep(self.duration*60)
      while self.duration > 0:
        # Sleeps for 1 minute 
        time.sleep(60)
        self.duration -= 1
        

      #Write stop event
      print "Transaction ID="+str(transactionID)
      cur = con.cursor()      
      cur.execute("UPDATE events SET stop_time=datetime('now','localtime')  WHERE row_id="+str(transactionID))
      con.commit()
      con.close()

      mx = ["end",str(self.zoneID), str(boardPin), time.strftime("%H:%M:%S")]
      #Write event in Logger
      self.writeLog(mx)
      
      # close GPIO
      GPIO.output(int(boardPin), GPIO.LOW)
    
    sys.exit(0)
    return
    
  
  def setParameters(self, runTime, zoneID, pinID):
    # Sets the parameter before instantiate the thread
    print "ZoneThread: setParameters Duration:%s Zone:%s" % (runTime,zoneID)
    self.duration=float(runTime)
    self.zoneID=int(zoneID)
    #self.pinID=pinIDr
    return
  
  
  def closeZone(self,zoneId):
    # Method to close the pins and so close valve 
    # setting GPIO mode
    GPIO.setmode(GPIO.BOARD) 
    
    # setting out  
    GPIO.setup(self.GPIOPin[zoneId], GPIO.OUT)

    # close all the pins
    GPIO.output(int(pin), GPIO.LOW)
    return
    
  def writeLog(self,msg):
    event = "1"

    logFile = open(self.logFilePath,"a") #open file in append mode
    logFile.write(msg[0] + " " + msg[1] + " " +msg[2] + " " + msg[3]+ "\n")
    logFile.close()

    logFile = open(self.logFileHTML,"a") #open file in append mode
    if msg[0] == "start":
        logFile.write("<TR><TD>"+msg[2]+"</TD><TD>"+msg[3]+"</TD>\n")
    else:
        logFile.write("<TD>"+msg[3]+"</TD></TR>\n")
        event = "0"
    logFile.close()


    return
    
