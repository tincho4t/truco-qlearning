


class Card(object):

	def __init__(self, dic):
		super(Card, self).__init__()
		self.suit = dic['suit']
		self.value = dic['value']
		