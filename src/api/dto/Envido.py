

class Envido(object):
	"""Represent the Envido's status
		{
            is_open: false,
            sung: ["Envido", "Envido", "RealEnvido"],
            oppenent_envido_score: 26
        }
	"""
	def __init__(self, dic):
		super(Envido, self).__init__()
		self.isOpen = dic['is_open']
		self.sung = dic['sung']
		self.oppenentEnvidoScore = dic['oppenent_envido_score']
	
	def isOpen(self):
		return self.isOpen

	def getSung(self):
		return self.sung

	def getOppenentEnvidoScore(self):
		return self.oppenentEnvidoScore
