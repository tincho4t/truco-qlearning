from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import json
import csv
import datetime
from urlparse import parse_qs
 
class PerformanceRequestHandler(BaseHTTPRequestHandler):
    """ Static variable that contains the destination where to post the results """
    save_folder = None

    """ Static variable that contains the mapping from ports to players """
    player_1_file = None
    player_2_file = None
    
    """ Static variable that indicates if a new performance has arrived  """
    performance_measured = False

    """ Static variable that indicates the current batch_number of the players  """
    batch_number = None

    def save_results(self, match_results):
        csv_file  = open(self.save_folder + '/results.csv', "a+")
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow([str(datetime.datetime.utcnow()), self.player_1_file, self.player_2_file, match_results['player_1_average_wins'], match_results['player_1_average_points'], self.batch_number])
        PerformanceRequestHandler.performance_measured = True
        print "Se paso a TRUE %d" % PerformanceRequestHandler.performance_measured

    def getBodyParameters(self):
        body_string = self.rfile.read(int(self.headers['Content-Length']))
        return json.loads(body_string)

    def getParsedPOSTParameters(self):
        return self.getBodyParameters()

    def do_POST(self):
        match_results = self.getParsedPOSTParameters()
        self.save_results(match_results)
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        return

    def do_OPTIONS(self):           
        self.send_response(200, "ok")       
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "application/json")
        self.send_header('Access-Control-Allow-Methods', 'POST, PUT, OPTIONS, PATCH, DELETE')
        self.send_header("Access-Control-Expose-Headers", "Access-Control-Allow-Origin")
        self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")

    def log_message(self, format, *args):
        return

