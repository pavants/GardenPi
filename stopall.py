from mod_python import apache
import utility
from Zones import Zones
from Zone import Zone
import cgi

def stop( req ):
	
  formValues = req.form
  req.content_type = "text/html"
  req.send_http_header()
  req.write(utility.getInclude("header"))
  zones=Zones()
  zones.loadValues()
  if formValues['zoneSelected'] == '99':
    for i in range( zones.count() ):
      zone=zones.getZoneByID(i)
      zone.stopZone()
    req.write("<H3>All Zones has been closed")
  else: 
    try:
      zone=zones.getZoneByID(int(formValues['zoneSelected'])-1)
      zone.stopZone()
      req.write("<H3>Zone <U>%s</U> has been closed" % (zone.description))
    except:
      req.write("<H3>Error Closing zone:" % (zone.description))
    
  req.write("</H3>")
  req.write(utility.getInclude("footer"))
  return ;
  
  
def index( req ):


	zones = Zones() 
	zones.loadValues()

	
	
	req.content_type = "text/html"
	req.send_http_header()
	req.write(utility.getInclude("header"))
	req.write("<P><H3>Select the zone you want to open and the desired duration\n")
	req.write("")
	req.write("</P>\n")

	
	req.write("<FORM NAME=""zone"" ACTION=""stopall/stop"">\n")
	req.write("Select Zone: <SELECT NAME=\"zoneSelected\">\n ")
	req.write("<OPTION VALUE=\"99\">STOP ALL\n")
	for zone in zones.getZones():
		req.write("""<OPTION VALUE="%s">%s\n""" % (zone.zoneid,zone.description))
	req.write("""\n\n""")
	req.write("</SELECT>\n")

	req.write("<INPUT TYPE=\"SUBMIT\" NAME=\"start\" VALUE=\"Stop\">\n")
	
	req.write("</FORM>\n")
		
	req.write(utility.getInclude("footer"))
	return ;
