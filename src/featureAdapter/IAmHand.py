

class IAmHand(object):
	size = 1
	def convert(self, requestDTO):
		return [1 if requestDTO.iAmHand else 0]

		