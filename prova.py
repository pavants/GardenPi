#from mod_python import apache
#def handler(req):
#  req.send_http_header()
#  req.write("HEllo World")
#  return apache.OK
def index(req):
	return "Test OK!";
