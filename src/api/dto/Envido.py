

class Envido(object):
	"""Represent the Envido's status
		{
            status: finished,
            sung: ["Envido", "Envido", "RealEnvido"],
            oppenent_envido_score: 26
        }
	"""
	def __init__(self, dic):
		super(Envido, self).__init__()
		self.status = dic['status']
		self.sung = dic['sung']
		self.oppenentEnvidoScore = dic['oppenent_envido_score']
	