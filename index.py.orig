# parameters: Dictionary, contains the field list
# - desc: field description
# - type: field type; values (t=text, n=number, hhmm = hour and minutes)
# - len: inputbox length

from mod_python import apache
import utility
import cgi

def index(req):


  req.content_type = "text/html;charset=utf-8"
  req.send_http_header()
  req.write(utility.getInclude("header"))

  
  
  req.write("<P><H3>Rasberry Pi Irrigation system status</H3><BR>Here are the last watering times \n<BR>")
  req.write("<TABLE WIDTH='80%'>\n")
  req.write("<THEAD><TR>")
  req.write("<TD><B>Zone</B></TD>\n")
  req.write("<TD><B>Start</B></TD>\n")
  req.write("<TD><B>Stop</B></TD>\n")
  req.write("</TR></THEAD>\n")
  try:
    req.write(open('/var/www/raspberry/irrigationLog.txt').read())
  except:
    req.write("<TR><TD COLSPAN=3 ALIGN=CENTER>no watering available</TD></TR>")
    
  req.write("</TABLE>\n")
  req.write("</TABLE>\n")
  req.write("</P>\n")

  req.write(utility.getInclude("footer"))
  return ;
