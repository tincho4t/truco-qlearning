from BaseHTTPServer import HTTPServer
import sys
sys.path.insert(0, '../player')
from player.Randomio import Randomio

class Webserver(object):
	"""docstring for Webserver"""
	def __init__(self, requestHandler):
		super(Webserver, self).__init__()
		self.requestHandler = requestHandler

	def run(self, port=8000):
		httpd = HTTPServer(('0.0.0.0', port), self.requestHandler)
		while True:
		    httpd.handle_request()
		