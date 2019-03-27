

class Action(object):
	TRUCO = "Truco"
	RETRUCO = "ReTruco"
	VALECUATRO = "ValeCuatro"
	QUIERO = "Quiero"
	NOQUIERO = "NoQuiero"
	ENVIDO = "Envido"
	REALENVIDO = "RealEnvido"
	FALTAENVIDO = "FaltaEnvido"
	PLAYCARDLOW = "PlayCardLow"
	PLAYCARDMIDDLE = "PlayCardMiddle"
	PLAYCARDHIGH = "PlayCardHigh"
	PLAYCARD = "PlayCard"

	POSSIBLE_ACTIONS = 11

	actionToIndexDic = {
		"Truco":0,
		"ReTruco":1,
		"ValeCuatro":2,
		"Quiero":3,
		"NoQuiero":4,
		"Envido":5,
		"RealEnvido":6,
		"FaltaEnvido":7,
		"PlayCardLow": 8,
		"PlayCardMiddle": 9,
		"PlayCardHigh": 10
	}

	actionToStringDic = {
		0:"Truco",
		1:"ReTruco",
		2:"ValeCuatro",
		3:"Quiero",
		4:"NoQuiero",
		5:"Envido",
		6:"RealEnvido",
		7:"FaltaEnvido",
		8:"PlayCardLow",
		9:"PlayCardMiddle",
		10:"PlayCardHigh"
	}