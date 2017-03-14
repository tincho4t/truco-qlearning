


class Card(object):
	"""
		possible suits: ["Cup", "Coin", "Club", "Sword"]
	"""
	def __init__(self, dic):
		super(Card, self).__init__()
		self.suit = dic['suit']
		self.value = dic['value']

	def toDic(self):
		return {
			"suit": self.suit,
			"value": self.value
		}
