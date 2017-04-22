import argparse
from player.QLearner import QLearner
from api.Webserver import Webserver
from api.QLearningRequestHandler import QLearningRequestHandler

parser = argparse.ArgumentParser()
parser.add_argument('-p','--port', help='Port', required=True)

def main(port):
	QLearningRequestHandler.player = QLearner()
	ws = Webserver()
	ws.run(port)

if __name__ == '__main__':
	args = vars(parser.parse_args())
	main(int(args['port']))
