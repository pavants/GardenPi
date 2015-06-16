# parameters: Dictionary, contains the field list
# - desc: field description
# - type: field type; values (t=text, n=number, hhmm = hour and minutes)
# - len: inputbox length

from mod_python import apache
import utility
import os
from Zones import Zones 
from Zone import Zone

def displayZone(req,nZone):
  zones = Zones()
  showValues = False
  # if configuration file  already created let's load the information from it
  # change the total Zone with the one read from the file
  #if int(nZone) == -1:
  zones.loadValues()
  nZone = zones.count()
  showValues = True
  htmlCode=""
  
  # load parameters for HTML, change this to change the fields 
  parameters={}
  parameters.update({'01_name':{'desc':'Zone Name: ','type':'t','len':'10'}})
  parameters.update({'02_description':{'desc':'Zone description: ','type':'t','len':'20'}})
  parameters.update({'03_imagearea':{'desc':'Image area for this zone.<BR> Put in order left, top, width and height, then color','type':'t','len':'25'}})
  parameters.update({'04_days':{'desc':'Weekdays (1 Monday, 2 Thuesday... 7 Sunday) ','type':'t','len':'12'}})
  parameters.update({'05_start':{'desc':'Start Time hh.mm 0-24 ','type':'hhmm','len':'5'}})
  parameters.update({'06_duration':{'desc':'Duration in minutes? ''','type':'n','len':'3'}})
  
  
  #preparing html
  htmlCode=utility.getInclude("header")
  htmlCode=htmlCode+"<FORM NAME=""zone"" METHOD='POST' ACTION=""config/saveParams"">\n"
  htmlCode=htmlCode+"<INPUT TYPE='hidden' NAME='nzone' VALUE='%s'>\n" % nZone
  htmlCode=htmlCode+"<TABLE ALIGN='CENTER' WIDTH=80% >\n"

  i=0
  keys =[]

  while  i < int(nZone):
    keys=parameters.keys()
    htmlCode=htmlCode+"<THEAD><TR><TD COLSPAN=2 ALIGN=CENTER><H3>Zone Number: %u</H3></TD></TR></THEAD>" % (i+1)
    keys.sort()
    
    #Looping on parameters
    for par in keys:
      #if configuration file exists show values
      if showValues:
        value = zones.getZoneByID(i).getValue(par[3:])
      else:
        value = ""
        
      if parameters[par]["type"] == "t":
        line="<TR><TD ALIGN=Left>%s</TD><TD><INPUT TYPE=TEXT NAME=\"%s\" SIZE=""%s"" MAXLENGTH=""%s"" VALUE=""%s""></TD></TR>\n" % (parameters[par]["desc"],par[3:],parameters[par]["len"],parameters[par]["len"],value)
      elif parameters[par]["type"] == "n":
        line="<TR><TD ALIGN=Left>%s</TD><TD><INPUT STYLE=""text-align:right"" TYPE=TEXT NAME=\"%s\" SIZE=""%s"" MAXLENGTH=""%s"" VALUE=""%s""></TD></TR>\n" % (parameters[par]["desc"],par[3:],parameters[par]["len"],parameters[par]["len"],value)
      elif parameters[par]["type"] == "hhmm":
        line="<TR><TD ALIGN=Left>%s</TD><TD><INPUT TYPE=TEXT NAME=\"%s\" SIZE=""%s"" MAXLENGTH=""%s"" VALUE=""%s""></TD></TR>\n" % (parameters[par]["desc"],par[3:],parameters[par]["len"],parameters[par]["len"],value)

      htmlCode=htmlCode+line
    
    i = i + 1 

  htmlCode=htmlCode+"<TR><TD COLSPAN=2 ALIGN=center><INPUT TYPE=""submit"" VALUE=""Save""></TD></TR>"
  htmlCode=htmlCode+"</TABLE>"

  # Writing page
  req.content_type = "text/html"
  req.send_http_header()
  req.write(htmlCode)
  req.write(utility.getInclude("footer"))
  nzone=0
  return 

  
def saveParams(req):
  htmlCode="<H3>Parameters correctly Saved</H3>\n<TABLE BORDER=1 WIDTH=100% ALIGN=CENTER>\n"
  fields=utility.getDefaultFields()
  data = req.form
  nzone = int(data['nzone'])-1
  config=[]
  i=0
  params = req.form
  while i <= nzone:
    zone={}
    #htmlCode=htmlCode+"<TR><TD COLSPAN=2>&nbsp</TD></TR>\n"
    htmlCode=htmlCode+"<TR><TH><B>Zone ID</B></TH><TH>%i </TH></TR>\n" % (i+1)
    zone.update({"zoneid":(i+1)}) 
    for key in fields:
      htmlCode=htmlCode+"<TR><TD><B>%s</B></TD><TD>%s</TD></TR>\n" % (key,data[key][i])
      zone.update({key:data[key][i]})
      
    config.append(zone)
    i=i+1
  utility.saveConfig2(config)
  htmlCode=htmlCode+"</TABLE>\n"


  req.content_type = "text/html"
  req.send_http_header()
  req.write(utility.getInclude("header"))
  req.write(htmlCode)
  req.write(utility.getInclude("footer"))
  return 
	
	
def index(req):

  if (not os.path.isfile("/var/www/raspberry/zones.cfg")):
    req.content_type = "text/html"
    req.send_http_header()
    req.write(utility.getInclude("header"))
    req.write("<FORM NAME=""zone"" ACTION=""config/displayZone"">")
    req.write("<P><H3>Rasberry Pi Irrigation system configuration</H3><BR>How you probably now often garden area are divided in zones to ")
    req.write("fit the available water flow. <BR>In the next step you will input the number of the zones and then describe each one ")
    req.write("and select start time, irrigation time and frequency during the week.</P>")

    req.write("<TABLE WIDTH=""20%"" ALIGN=center>")
    req.write("<TR>")
    req.write("<TD ALIGN=""center"">How many Zones ? <SELECT NAME=""nZone"">")
    req.write("<OPTION NAME=\"1\">1")
    req.write("<OPTION NAME=\"2\">2")
    req.write("<OPTION NAME=\"3\">3")
    req.write("<OPTION NAME=\"4\">4")
    req.write("</SELECT>")
    req.write("</TD>")
    req.write("</TR>")
    req.write("<TR>")
    req.write("<TD ALIGN='CENTER'>")
    req.write("<INPUT TYPE='SUBMIT' VALUE='Next >'>")
    req.write("</TD>")
    req.write("</TR>")
    req.write("</TABLE>")
    req.write(utility.getInclude("footer"))
  else:
    displayZone(req,-1)
  return 
