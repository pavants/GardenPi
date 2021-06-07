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
  duration=float(data["minutes"])

  zones=Zones()
  zones.loadValues()
  #req.write(str(duration)+"<BR>")
  openZones=[]
  for item in data:
    if item.find("chk-") > -1:
      req.write(item+"<BR>")
      openZones.append(item[item.find("-")+1:])

  if len(openZones) > 1:
    zones.startMultiple(duration,openZones)
    req.write("<H3>Task Running, opening zones for %i minutes \n" % (duration))
  else:
    zone = zones.getZoneByID(int(openZones[0])-1)
    zone.startZone(duration)
    req.write("<H3>Task Running, opening zones for %i minutes \n" % (duration))
    
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
  req.write("<fieldset data-role=\"controlgroup\">\n ")
  req.write("<legend>Select Zone: </legend>\n ")
  #req.write("Select Zone: <SELECT NAME=\"zoneSelected\">\n ")
  for zone in zones.getZones():
        zoneId          =zone.zoneid
        zoneDescription =zone.description
  	req.write("<input name=chk-%s id=chk-%s TYPE=checkbox data-mini=true>\n" % (zoneId,zoneId))
	req.write("<label for=\"chk-"+zoneId+"\">"+zoneDescription+"</label>\n")
  req.write("</FIELDSET>\n ")
  
  req.write("\n\n")
  req.write("</SELECT>\n")
  req.write("<label for=\"duration\">Minutes:&nbsp&nbsp</label>")
  req.write("<input type=\"range\" name=\"minutes\" id=\"minutes\" value=\"5\" min=\"2\" max=\"20\" data-show-value=\"true\">\n<BR>\n")
  req.write("<INPUT TYPE=\"SUBMIT\" data-inline=\"true\" NAME=\"start\" VALUE=\"Start\">\n")
  req.write("</FORM>\n")
  	
  req.write(utility.getInclude("footer"))
  return ;
