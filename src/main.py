from player.QLearner import QLearner
from api.Webserver import Webserver
from api.QLearningRequestHandler import QLearningRequestHandler

def main():
	QLearningRequestHandler.player = QLearner()
	ws = Webserver()
	ws.run()

if __name__ == '__main__':
	main()
