from mod_python import apache
import utility
import cgi
from Zones import Zones 
from Zone import Zone

def startZone(req):

  data = req.form
  req.content_type = "text/html"
  req.send_http_header()
  req.write(utility.getInclude("header"))

  zones=Zones()
  zones.loadValues()

  zone=zones.getZoneByID(int(data['zoneSelected'])-1)
  
  req.write(zone.getValue('description'))
  req.write("<P>")
  #send to server the request to open a zone
  result=zone.startZone(data['minutes'])

  if ( result == "open"):
    req.write("<H3>Starting Zone: %s for %s minutes \n" % (data['zoneSelected'],data['minutes']))
    req.write("</H3>")
  else:
    req.write("<H3>Error: %s Opening Zone: %s \n" % (result,data['zoneSelected']))
    req.write("</H3>")
    
  req.write("</P>\n")
  req.write(utility.getInclude("footer"))

	
def index(req):


	zones = Zones() 
	zones.loadValues()

	
	
	req.content_type = "text/html"
	req.send_http_header()
	req.write(utility.getInclude("header"))
	req.write("<P><H3>Select the zone you want to open and the desired duration\n")
	req.write("")
	req.write("</P>\n")

	
	req.write("<FORM NAME=""zone"" ACTION=""manual/startZone"">\n")
	req.write("Select Zone: <SELECT NAME=\"zoneSelected\">\n ")
	for zone in zones.getZones():
		req.write("""<OPTION VALUE="%s">%s\n""" % (zone.zoneid,zone.name))
	req.write("""\n\n""")
	req.write("</SELECT>\n")

	req.write("&nbspDuration (minutes):<INPUT TYPE=\"TEXT\" NAME=\"minutes\" VALUE=\"30\" SIZE=\"2\">\n&nbsp&nbsp&nbsp&nbsp")
	req.write("<INPUT TYPE=\"SUBMIT\" NAME=\"start\" VALUE=\"Start\">\n")
	
	req.write("</FORM>\n")
		
	req.write(utility.getInclude("footer"))
	return ;
