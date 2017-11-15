from BaseHTTPServer import HTTPServer
from ApiPlayerRequestHandler import ApiPlayerRequestHandler

class Webserver(object):

	def run(self, port=8000):
		httpd = HTTPServer(('0.0.0.0', port), ApiPlayerRequestHandler)
		while True:
		    httpd.handle_request()
		