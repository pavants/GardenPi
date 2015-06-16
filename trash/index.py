# parameters: Dictionary, contains the field list
# - desc: field description
# - type: field type; values (t=text, n=number, hhmm = hour and minutes)
# - len: inputbox length

from mod_python import apache
import utility
import cgi


def displayZone(req,nZone):
	parameters={}
	parameters.update({'06_duration':{'desc':'Duration in minutes? ''','type':'n','len':'3'}})
	parameters.update({'05_start':{'desc':'Start Time hh.mm 0-24 ','type':'hhmm','len':'5'}})
	parameters.update({'04_days':{'desc':'Weekdays (1 Monday, 2 Thuesday... 7 Sunday) ','type':'t','len':'7'}})
	parameters.update({'02_description':{'desc':'Zone description: ','type':'t','len':'20'}})
	parameters.update({'01_name':{'desc':'Zone Name: ','type':'t','len':'10'}})
	parameters.update({'03_imagearea':{'desc':'Image area for this zone.<BR> Point top left xy and Point bottom right xy (x,y,x,y)','type':'t','len':'15'}})
	print nZone
	keys =[]
	outputVal=parameters.copy()
	htmlCode=""

	req.content_type = "text/html"
	req.send_http_header()
	
	req.write(htmlCode)
	req.write("<TR><TD COLSPAN=2 ALIGN=center><INPUT TYPE=""submit"" VALUE=""Save""></TD></TR>")
	req.write("</TABLE>")
	req.write(utility.getInclude("footer"))
	return 
	
	
#metodo richiamato dal Form
def saveParams(req):
	s=""
	fields=utility.getDefaultFields()
	data = req.form
	nzone = int(data['nzone'])-1
	config=[]
	req.content_type = "text/html"
	req.send_http_header()
	i=0
	params = req.form
	req.write("%s"%params['name'][0])
	 
	while i <= nzone:
		zone={}
		for key in fields:
			req.write("%s=%s\n"%(key,data[key][i]))
			zone.update({key:data[key][i]})
			
		config.append(zone)
		i=i+1
	utility.saveConfig2(config)
	return s	
	
	
	s=utility.getInclude("header")
	top = data['nzone']
	s=s+"top : %s " % top
	i=1
	while i <= int(top):
		x=0
		while x < len(fields):
			field=fields[x]+str(i)
			s=s+"%s %s " % (field, data[field])
			x=x+1
		i=i+1
	#utility.writeFile(data)
	s=s+"<H3>Parameters correctly Saved</H3>"
	s=s+utility.getInclude("footer")
	
	return s
	
	
def index(req):

  #Parameters for temp and humidity sensors:

  fields=utility.getDefaultFields()
  area  =utility.getConfigParameter("imagearea")
  req.content_type = "text/html"
  req.send_http_header()
  req.write(utility.getInclude("header"))
  #req.write("<FORM NAME=""zone"" ACTION=""config/displayZone"">\n")
  req.write("<P><H3>Rasberry Pi Irrigation system status</H3><BR>Here you can see what is happening on your Garden controller... \n")
  req.write("")
  req.write("</P>\n")


  req.write("<DIV>")
  for valArea in area:
    _left  = valArea.split(",")[0]
    _top   = valArea.split(",")[1]
    _width = valArea.split(",")[2]
    _height= valArea.split(",")[3]
    _color= valArea.split(",")[4]
    #req.write("""<span style="position: relative; display: block; left:%spx;top:%spx;width:%spx;height:%spx;border:1px solid #000;background:%s;">testo</SPAN>\n""" % (_left,_top,_width,_height,_color))
  #req.write("""<div style="position:static;left:71px;top:157px;width:274px;height:56px;border:1px solid #000;background:green;">This is a rectangle! </DIV>""")
  req.write("""\n\n""")
  req.write("</DIV>")

  req.write(utility.getInclude("footer"))
  return ;
