#####
#####
import sys
sys.path.append("/var/www/raspberry/service")
from mod_python import apache
import utility
import cgi
from  datetime import date
import datetime
import sqlite3 as lite
import time
from GardenPi import GardenPi


def save(req):
  
  cfg = GardenPi()
  dbName = cfg.dbName
  req.content_type = "text/html;charset=utf-8"
  req.send_http_header()
  req.write(utility.getInclude("header"))
  dateOff = req.form["dateoff"].split("/")
  dateOffsql = dateOff[2]+dateOff[1]+dateOff[0]
  postedData = req.form
  sqlCmd="INSERT INTO dayoff VALUES ('%s');"  % dateOffsql

  #req.write(sqlCmd)
  #req.write(dbName)
  conn = lite.connect(dbName)
  cur = conn.cursor()
  cur.execute(sqlCmd)
  conn.commit()

  
  req.write("""
  <P>
  save done, on <B>%s</B> I will not rain on garden !
  </P>
  <P>Next Day OFF:<BR>
  """ % req.form["dateoff"])
  cur.execute("SELECT when_stop FROM dayoff WHERE when_stop > '"+time.strftime("%Y%m%d")+"' ORDER BY 1; ")
  for record in cur:
      dayoff=record[0]
      req.write(dayoff[6:]+"/"+dayoff[4:6]+"/"+dayoff[0:4]+" <BR>")
    
  req.write(utility.getInclude("footer"))
  conn.close()
  return

def index(req):

  req.content_type = "text/html;charset=utf-8"
  req.send_http_header()
  req.write(utility.getInclude("header"))
  
  tomorrow = date.today()
  tomorrow = tomorrow + datetime.timedelta(days=1)

  req.write("""
    <FORM NAME="dataoff" METHOD="POST" ACTION="stopday/save"> 
    <label for="dateoff">First name:</label>
    <input type="text" name="dateoff" id="dateoff" VALUE="%s">   
    <input type="submit" name="send" id="send" VALUE="Save">   
    </FORM>
     
   """ % tomorrow.strftime("%d/%m/%Y") )
  return ;

