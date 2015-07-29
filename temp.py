from mod_python import apache
import utility
import cgi
import datetime
from test.test_support import temp_cwd

def index(req):


  fields=utility.getDefaultFields()
  area  =utility.getConfigParameter("imagearea")
  req.content_type = "text/html"
  req.send_http_header()
  req.write(utility.getInclude("header"))
  req.write("<P><H3>Rasberry Pi Irrigation system status</H3><BR>Here are the last read temperature  \n<BR>")
  req.write("<TABLE WIDTH='80%'>\n")
  req.write("<THEAD><TR>")
  req.write("<TD><B>Date</B></TD>\n")
  req.write("<TD><B>Time</B></TD>\n")
  req.write("<TD><B>Temperature</B></TD>\n")
  req.write("<TD><B>Rel. Humidity</B></TD>\n")
  req.write("</TR></THEAD>\n")
  try:
    f = open('/var/www/raspberry/tempLog.txt',"r")
    content = f.read().splitlines()
    content = sorted(content,reverse=True)
    for line in content: 
      tDate,tTime,temp,hum=line.split() 
      req.write("<TR>")
      req.write("<TD>"+tDate[6:8]+"/"+tDate[4:6]+"/"+tDate[0:4]+"</TD>")
      req.write("<TD>"+tTime[0:2]+":"+tTime[2:4]+":"+tTime[4:6]+"</TD>")
      req.write("<TD>"+temp+"</TD>")
      req.write("<TD>"+hum+"</TD>")
      req.write("</TR>\n")
    req.write("</TD></TR>")
  except:
    req.write("<TR><TD COLSPAN=4 ALIGN=CENTER>no temperature log available</TD></TR>")
    
  req.write("</TABLE>\n")
  req.write("</TABLE>\n")
  req.write("</P>\n")

  req.write(utility.getInclude("footer"))
  return ;
