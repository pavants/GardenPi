#index of GardenPi application
#author Michele Pavan michele.pavan@gmail.com
#date   2013

import cherrypy
import os, os.path
import utility

class Raspberry:
    @cherrypy.expose
    def index(self):
         
        
        return utility.getInclude("header")+"""
  
        <P><H3>Rasberry Pi Irrigation system status</H3><BR>Here are the last watering times \n<BR>
        <TABLE WIDTH='80%'>\n
        <THEAD><TR>
        <TD><B>Event</B></TD>\n
        <TD><B>Zone</B></TD>\n
        <TD><B>Time</B></TD>\n
        </TR></THEAD>\n
        </TABLE>\n
        </TABLE>\n
        </P>\n"""+utility.getInclude("footer")
        #+open('/var/www/raspberry/irrigationLog.txt').read()+"""

    @cherrypy.expose
    def about(self):
        return """
    <P>This application is created under licence GNUGPL2 and is free distributable maintaining the name of the author</P>
    <P>The CSS stylesheet was created by Erwin Aligam for this website http://www.styleshout.com/</P>
    <P>If you like this application you can feel free to write to the author: <A HREF="mailto:michele.pavan@gmail.com">Michele Pavan</A></P>
    <P>Or leave a post on <A HREF="http://mplifetime.blogspot.com">http://mplifetime.blogspot.com</A></P>
  """

    
    index.exposed = True
    
    
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
    #print os.path.dirname(__file__)
    configfile = os.path.join(os.path.dirname(__file__),'server.conf')  
    cherrypy.quickstart(Raspberry(),'/' ,  configfile)
    