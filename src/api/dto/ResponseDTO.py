

class ResponseDTO(object):

	def __init__(self):
		self.action = None
		self.card = None
	
	def setAction(self, action):
		self.action = action

	def setCard(self, card):
		self.card = card

	def toDic(self):
		return {
			"action": self.action,
			"card": self.card.toDic() if self.card != None else None
		}

