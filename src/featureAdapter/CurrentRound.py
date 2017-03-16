

class CurrentRound(object):
	size = 1
	def convert(self, requestDTO):
		return [requestDTO.getCurrentRound()]