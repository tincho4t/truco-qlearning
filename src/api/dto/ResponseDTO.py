

class ResponseDTO(object):
	
	def setAction(self, action):
		self.action = action

	def setCard(self, card):
		self.card = card

	def toDic(self):
		return {
			"action": self.action,
			"card": self.card
		}
