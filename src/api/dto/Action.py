

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
	PLAYCARDLOW = "PlayCardLow"
	PLAYCARDMIDDLE = "PlayCardMiddle"
	PLAYCARDHIGH = "PlayCardHigh"

	actionToIndexDic = {
		"Truco":0,
		"ReTruco":1,
		"ValeCuatro":2,
		"Quiero":3,
		"NoQuiero":4,
		"PlayCard":5,
		"PostScore":6,
		"SonBuenas":7,
		"Envido":8,
		"RealEnvido":9,
		"FaltaEnvido":10,
		"GoToDec":11,
		"PlayCardLow": 12,
		"PlayCardMiddle": 13,
		"PlayCardHigh": 14
	}

	actionToStringDic = {
		0:"Truco",
		1:"ReTruco",
		2:"ValeCuatro" ,
		3:"Quiero",
		4:"NoQuiero" ,
		5:"PlayCard",
		6:"PostScore" ,
		7:"SonBuenas",
		8:"Envido",
		9:"RealEnvido" ,
		10:"FaltaEnvido",
		11:"GoToDec",
		12:"PlayCardLow",
		13:"PlayCardMiddle",
		14:"PlayCardHigh"
	}