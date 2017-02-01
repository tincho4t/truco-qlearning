from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import json
from urlparse import parse_qs
from dto.RequestDTO import RequestDTO
 
class QLearningRequestHandler(BaseHTTPRequestHandler):
    
    """
        Parse the query string parameters.
    """
    def getParameters(self):
        queryString = ""
        parts = self.path.split('?', 1)
        if len(parts) == 2:
            queryString = parts[1]
        return parse_qs(queryString)

    def getBodyParameters(self):
        body_string = self.rfile.read(int(self.headers['Content-Length']))
        return json.loads(body_string)

    def getParsedParameters(self):
        return RequestDTO(self.getBodyParameters())
        # return RequestDTO(self.getParameters())

    def do_POST(self):
        response = self.play(self.getParsedParameters())
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({'data': str(response)}))
        return
