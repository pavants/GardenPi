import utility


def index( req ):
	
	req.content_type = "text/html"
	req.send_http_header()
	req.write(utility.getInclude("header"))
	req.write("""
    <P>This application is created under licence GNUGPL2 and is free distributable maintaining the name of the author</P>
    <P>The CSS stylesheet was created by Erwin Aligam for this website http://www.styleshout.com/</P>
    <P>If you like this application you can feel free to write to the author: <A HREF="mailto:michele.pavan@gmail.com">Michele Pavan</A></P>
    <P>Or leave a post on <A HREF="http://mplifetime.blogspot.com">http://mplifetime.blogspot.com</A></P>
  """)

	req.write(utility.getInclude("footer"))
	return ;
