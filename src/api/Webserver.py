from BaseHTTPServer import HTTPServer
from QLearningRequestHandler import QLearningRequestHandler

class Webserver(object):

	def run(self, port=8000):
		httpd = HTTPServer(('0.0.0.0', port), QLearningRequestHandler)
		while True:
		    httpd.handle_request()
		