from multiprocessing.connection import Client
from array import array
from GardenPi import GardenPi
import sys

#address = ('localhost',1909)
#address = ('192.168.1.114',1909)
cfg = GardenPi()
address = (cfg.ipaddress,cfg.port)
print address

authKey = cfg.authkey
print authKey

if len(sys.argv) == 1:
  print "Usage: \n       python client.py [pin:duration] \n       python client.py [close] to close server."
  exit()

conn = Client(address, authkey = authKey)
print conn
conn.send(sys.argv[1])

conn.close()
