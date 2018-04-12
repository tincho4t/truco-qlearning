import argparse
from player.QLearner import QLearner
from player.RulePlayer import RulePlayer
from api.Webserver import Webserver
from api.ApiPlayerRequestHandler import ApiPlayerRequestHandler

parser = argparse.ArgumentParser()
parser.add_argument('-p','--port', help='Port', required=True)
parser.add_argument('-f','--file', help='Algo File', required=False)
parser.add_argument('-n','--name', help='Algo Name', required=False)
parser.add_argument('-hi','--hidden', help='Hidden Layer Size', required=False)
parser.add_argument('-l','--learn', help='Learn (y/n)', required=False)
parser.add_argument('-r','--rule', help='Flag for rule based player', required=False)

def main(port, player):
	ApiPlayerRequestHandler.player = player
	ws = Webserver()
	ws.run(port)

if __name__ == '__main__':
	args = vars(parser.parse_args())
	port = int(args['port'])
	player = None
	if 'file' in args and args['file'] is not None:
		if 'hidden' in args and args['hidden'] is not None:
			player = QLearner(args['name'], args['file'], args['hidden'], args['learn'])
		else:
			player = QLearner(args['name'], args['file'])
	elif 'rule' in args and args['rule'] is not None:
		player = RulePlayer()
	else:
		player = QLearner(args['name'])

	main(port, player)
