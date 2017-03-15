

class Action(object):
	TRUCO = "Truco"
	RETRUCO = "ReTruco"
	VALECUATRO = "ValeCuatro"
	QUIERO = "Quiero"
	NOQUIERO = "NoQuiero"
	PLAYCARD = "PlayCard"
	POSTSCORE = "PostScore"
	SONBUENAS = "SonBuenas"
	ENVIDO = "Envido"
	REALENVIDO = "RealEnvido"
	FALTAENVIDO = "FaltaEnvido"
	GOTODECK = "GoToDec"

	_actionIndex = {
		"Truco":1
		"ReTruco":2
		"ValeCuatro":3 
		"Quiero":4
		"NoQuiero":5 
		"PlayCard":6
		"PostScore":7 
		"SonBuenas":8
		"Envido":9
		"RealEnvido":10 
		"FaltaEnvido":11
		"GoToDec":12
	}

	def getIndex(self, actionString):
		return _actionIndex[actionString]
