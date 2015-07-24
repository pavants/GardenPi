#from mod_python import apache
import ConfigParser
import sys
#import debug

#cfgFileName='/usr/local/share/pi/zones.cfg'
#cfgFileName='/data/gardenpi/zones.cfg'
cfgFileName='/var/www/cherry/zones.cfg'

def getInclude(part):
	fileName="/var/www/cherry/%s.inc" % part
	fHeader=open(fileName,'r')
	header = fHeader.read()
	fHeader.close()
	return header


def saveConfig2(zones):
	#cfgFileName='/usr/local/share/pi/zones.cfg'
	config=ConfigParser.RawConfigParser()
	
	i=0
	while i < len(zones):
		section="Zona %u" % (i+1)
		config.add_section(section )
		for key in zones[i]:
			config.set(section,key,zones[i].get(key))
		i=i+1
		
	with open(cfgFileName,'wb') as configfile:
		config.write(configfile)
	
	return
	
def getDefaultFields():
	return ['name','description','imagearea','days','start','duration']


def getConfig():
	#restituisce un dictionary della zona con i parametri relativi
	#cfgFileName='/usr/local/share/pi/zones.cfg'
	config=ConfigParser.RawConfigParser()
	
	return
	
def getConfigParameter(name):
	#carica il file zone e restituisce un array con il valore del parametro passato
	values = []
	
	config=ConfigParser.RawConfigParser()
	config.read(cfgFileName)
	
	for section in config.sections():
		values.append(config.get(section,name))
	return values
	
def IrrigationProcess():
	
	#cfgFileName='/usr/local/share/pi/zones.cfg'
	config=ConfigParser.RawConfigParser()
	config.read(cfgFileName)
	zones=config.sections()
	
	for key in zones:
		sys.stdout.write(key)

	return
