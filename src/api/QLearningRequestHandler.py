from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import json
from urlparse import parse_qs
from dto.GameStatusDTO import GameStatusDTO
from dto.LearnDTO import LearnDTO
 
class QLearningRequestHandler(BaseHTTPRequestHandler):
    """ Static variable that contains the q-player """
    player = None
    
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

    def getParsedPOSTParameters(self):
        return GameStatusDTO(self.getBodyParameters())

    def getParsedPUTParameters(self):
        return LearnDTO(self.getBodyParameters())

    def do_POST(self):
        response = QLearningRequestHandler.player.play(self.getParsedPOSTParameters())
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(response.toDic()))
        return

    def do_PUT(self):
        response = QLearningRequestHandler.player.learn(self.getParsedPUTParameters())
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps("OK"))
        return

    def do_OPTIONS(self):           
        self.send_response(200, "ok")       
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "application/json")
        self.send_header('Access-Control-Allow-Methods', 'POST, PUT, OPTIONS')
        self.send_header("Access-Control-Expose-Headers", "Access-Control-Allow-Origin")
        self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
