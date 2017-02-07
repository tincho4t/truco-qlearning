

class IAmHand(object):

	def convert(self, requestDTO):
		return [1 if requestDTO.iAmHand else 0]

		