from player.Randomio import Randomio
from api.Webserver import Webserver
from api.QLearningRequestHandler import QLearningRequestHandler

def main():
	QLearningRequestHandler.player = Randomio()
	ws = Webserver()
	ws.run()

if __name__ == '__main__':
	main()
