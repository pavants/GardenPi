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
  ### Internal Temp last 12 hrs
  ###################### 

  req.write("<TABLE>")
  req.write("<THEAD><TD><B>Last 12 temperatures and Humidity</B></TD></THEAD>")
  req.write("<THEAD><TD><B>Date</B></TD><TD><B>Temp</B></TD><TD><B>Humidity</TD></THEAD>")

  sqlCmd="SELECT detection_time,temperature, Humidity FROM temperature ORDER BY detection_time DESC LIMIT 12"
  cur.execute(sqlCmd)
  
  rows = cur.fetchall()
  cRow = 1
  if len(rows) >=1 :
    for row in rows:

        req.write("<TR>")
        req.write("<TD>"+row[0]+"</TD>")
        req.write("<TD>"+str(int(row[1]))+"</TD>")
        req.write("<TD>"+str(int(row[2]))+"</TD>")
        req.write("</TR>")
        cRow = cRow +1

  else:
    req.write("<TR><TD COLSPAN=4 ALIGN=CENTER>no temperature log available</TD></TR>")

  req.write("</TABLE>\n")
  req.write("</P>\n")




  sqlCmd="""
    SELECT T0.detection_time data_rif, T0.t_max, T1.t_min,T2.hum
    FROM (
    SELECT strftime('%Y%m%d',detection_time) detection_time, MAX(temperature)  t_max
          FROM temperature 
	  GROUP BY strftime('%Y%m%d',detection_time) ORDER BY 1 DESC LIMIT 10
	    ) T0,
		(
    SELECT strftime('%Y%m%d',detection_time) detection_time, MIN(temperature)  t_min
          FROM temperature 
	  GROUP BY strftime('%Y%m%d',detection_time) ORDER BY 1 DESC LIMIT 10
	    ) T1,
		(
     SELECT strftime('%Y%m%d',detection_time) detection_time, AVG(humidity)  hum
          FROM temperature 
	  GROUP BY strftime('%Y%m%d',detection_time) ORDER BY 1 DESC LIMIT 10
	    ) T2
   WHERE 
	T0.detection_time = T1.detection_time AND
	T0.detection_time = T2.detection_time 
	GROUP BY data_rif ORDER BY 1 DESC;
   """ 
  cur.execute(sqlCmd)
  
  rows = cur.fetchall()

  req.write("<TABLE><THEAD><TD><B>Date</B></TD><TD><B>Max</B></TD><TD><B>Min</B></TD><TD><B>Average</TD></THEAD>")
  #req.write("<TABLE BORDER=1><THEAD><TD>Date</TD><TD>Max</TD><TD>Min</TD><TD>Average</TD><TD></TD></THEAD>")
  cRow = 1
  if len(rows) >=1 :
    for row in rows:
        if (cRow % 2) == 0:
  	   color="yellow"
        else:
	   color="orange"
     
	req.write("<TR BGCOLOR="+color+">")
	req.write("<TD>"+row[0]+"</TD>")
	req.write("<TD>"+str(int(row[1]))+"</TD>")
	req.write("<TD>"+str(int(row[2]))+"</TD>")
	#req.write("<TD>"+str(int(row[3]))+"</TD>")
        req.write("<TD><IMG SRC='images/bar_hz.png' TITLE="+str(int(row[3]))+" HEIGHT=13 WIDTH="+str(int(row[1])*2)+"></TD>")
        #req.write("<TD STYLE='bgcolor:blue' WIDTH="+str(int(row[1])*2)+"></TD>")
	req.write("</TR>")
        cRow = cRow +1

  else:
    req.write("<TR><TD COLSPAN=4 ALIGN=CENTER>no temperature log available</TD></TR>")
    
  req.write("</TABLE>\n")
  req.write("</P>\n")
  conn.close()


  req.write(utility.getInclude("footer"))
  return ;
