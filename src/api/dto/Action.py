

class Action(object):
	TRUCO = "Truco"
	RETRUCO = "ReTruco"
	VALECUATRO = "ValeCuatro"
	QUIERO = "Quiero"
	NOQUIERO = "NoQuiero"
	PLAYCARDLOW = "PlayCardLow"
	PLAYCARDMIDDLE = "PlayCardMiddle"
	PLAYCARDHIGH = "PlayCardHigh"
	PLAYCARD = "PlayCard"
	POSTSCORE = "PostScore"
	SONBUENAS = "SonBuenas"
	ENVIDO = "Envido"
	REALENVIDO = "RealEnvido"
	FALTAENVIDO = "FaltaEnvido"
	GOTODECK = "GoToDec"

	_actionToIndex = {
		"Truco":1,
		"ReTruco":2,
		"ValeCuatro":3,
		"Quiero":4,
		"NoQuiero":5,
		"PlayCard":6,
		"PostScore":7,
		"SonBuenas":8,
		"Envido":9,
		"RealEnvido":10,
		"FaltaEnvido":11,
		"GoToDec":12,
		"PlayCardLow": 13,
		"PlayCardMiddle": 14,
		"PlayCardHigh": 15
	}

	_actionToString = {
		1:"Truco",
		2:"ReTruco",
		3:"ValeCuatro" ,
		4:"Quiero",
		5:"NoQuiero" ,
		6:"PlayCard",
		7:"PostScore" ,
		8:"SonBuenas",
		9:"Envido",
		10:"RealEnvido" ,
		11:"FaltaEnvido",
		12:"GoToDec",
		13:"PlayCardLow",
		14:"PlayCardMiddle",
		15:"PlayCardHigh"
	}

	def getIndex(self, actionString):
		return _actionToIndex[actionString]

	def getAction(self, actionIndex):
		return _actionToString[actionIndex]
