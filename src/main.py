from player.Randomio import Randomio
from api.Webserver import Webserver

def main():
	ws = Webserver(Randomio)
	ws.run()

if __name__ == '__main__':
	main()
