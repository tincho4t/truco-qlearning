


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

	def __eq__(self, other):
	    """Override the default Equals behavior"""
	    if isinstance(other, self.__class__):
	        return self.__dict__ == other.__dict__
	    return False

	def __ne__(self, other):
	    """Define a non-equality test"""
	    return not self.__eq__(other)

	def __str__(self):
		return str(self.value) + " of " + self.suit