import syslog
import time 
syslog.syslog("running %i %i" % (time.localtime()[3],time.localtime()[4]))
