import argparse
from player.QLearner import QLearner
from api.Webserver import Webserver
from api.QLearningRequestHandler import QLearningRequestHandler

parser = argparse.ArgumentParser()
parser.add_argument('-p','--port', help='Port', required=True)
parser.add_argument('-f','--file', help='Algo File', required=False)

def main(port, file):
	QLearningRequestHandler.player = QLearner(file)
	ws = Webserver()
	ws.run(port)

if __name__ == '__main__':
	args = vars(parser.parse_args())
	file = None
	if 'file' in args:
		file = args['file']
	main(int(args['port']), file)
