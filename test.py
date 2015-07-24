# parameters: Dictionary, contains the field list
# - desc: field description
# - type: field type; values (t=text, n=number, hhmm = hour and minutes)
# - len: inputbox length

import cherrypy
import os, os.path
import utility
from Zones import Zones 
from Zone import Zone

#from twisted.scripts.htmlizer import footer

class Raspberry:
    zones = Zones() 
    zones.loadValues()
    options = "" 

    for zone in zones.getZones():
        options = "<OPTION VALUE="+zone.zoneid+">"+zone.name+"\n"+options 
    header = """
        <body>
        <!DOCTYPE html>
        <html>
            <head>
            <title>GardenPi Irragation</title>
            <link rel="stylesheet" href="http://code.jquery.com/mobile/1.0a1/jquery.mobile-1.0a1.min.css" />
            <script src="http://code.jquery.com/jquery-1.4.3.min.js"></script>
            <script src="http://code.jquery.com/mobile/1.0a1/jquery.mobile-1.0a1.min.js"></script>
        
            <!-- jQMDateBox DateTime Picker module-->
            <link rel="stylesheet" type="text/css" href="http://cdn.jtsage.com/datebox/latest/jqm-datebox.min.css">
            <script type="text/javascript" src="http://cdn.jtsage.com/datebox/latest/jqm-datebox.core.min.js"></script>
            <script type="text/javascript" src="http://dev.jtsage.com/cdn/datebox/latest/jqm-datebox.mode.flipbox.min.js"></script>
        
        <script>
        $(document).on("pagecreate","#rain",function(){
        
        }
        </script>
        
        
        </head>
        <body>
        <div data-role="page">
        
            <div data-role="header">
                <h1>Raspberry Irrigation System</h1>
                <ul data-role="listview" data-inset="true">
                    <li><a href="#stopall">Stop All</a></li>
                    <li><a href="#manual">Stop All</a></li>
                    <li><a href="#rain">Rain Log</a></li>
                </ul>
            </div>
            <div data-role="content"></div>
            <div data-role="footer">
            </div>
        </div><!-- /page -->

        <div data-role="page" id="stopall">
        
            <div data-role="header">
                <h1>STOP ALL</h1>
            </div>
            <div data-role="content"></div>
            <div data-role="footer">
            </div>
        </div><!-- /page -->
        
        
        <div data-role="page" id="manual">
        
            <div data-role="header">
                <h1>Manual</h1>
            </div>
            <div data-role="content"></div>
            <FORM NAME=""zone"" ACTION=""manual/startZone"">
            Select Zone: <SELECT NAME=\"zoneSelected\">
    """+options+"""
            </SELECT>\n
            Duration (minutes):<INPUT TYPE=\"TEXT\" NAME=\"minutes\" VALUE=\"30\" SIZE=\"2\">
            <INPUT TYPE=\"SUBMIT\" NAME=\"start\" VALUE=\"Start\">
    
            </FORM>"""

              
    footer = """     
        
        </body>
        </html>
        """

    
    @cherrypy.expose
    def index(self):
        
        return self.header+"Page Content"+self.footer
            
    
    @cherrypy.expose
    def stopall(self):
        return self.header+"Stop All "+self.footer
    
    @cherrypy.expose
    def rain(self):
        return """--> rain <--"""
    
    
if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    #configfile = os.path.join(os.path.dirname(__file__),'server.conf'), '/' ,conf  
    cherrypy.quickstart(Raspberry(),'/',conf)
    
