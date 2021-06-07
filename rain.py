#####
#####
#from mod_python import apache
import utility
import cgi
import datetime
import sqlite3 as lite
from test.test_support import temp_cwd

def index(req):

  req.content_type = "text/html;charset=utf-8"
  req.send_http_header()
  req.write(utility.getInclude("header"))

  conn = lite.connect("/data/gardenpi/gardenpi.db") 
  cur = conn.cursor()
  ######################
  ### Last  12 rain  event
  ###################### 

  req.write("<TABLE>")
  req.write("<THEAD><TD><B>Last 12 rain events</B></TD></THEAD>")
  req.write("<THEAD><TD><B>Date time</B></TD></THEAD>")

  sqlCmd="SELECT rain_time FROM rain  ORDER BY rain_time DESC LIMIT 12"
  cur.execute(sqlCmd)
  
  rows = cur.fetchall()
  cRow = 1
  if len(rows) >=1 :
    for row in rows:

        req.write("<TR>")
        req.write("<TD>"+row[0]+"</TD>")
        req.write("</TR>")
        cRow = cRow +1

  else:
    req.write("<TR><TD ALIGN=CENTER>no rain</TD></TR>")

  req.write("</TABLE>\n")
  req.write("</P>\n")

  conn.close()


  req.write(utility.getInclude("footer"))
  return ;
