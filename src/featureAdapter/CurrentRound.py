from __future__ import division

class CurrentRound(object):
	size = 1
	def convert(self, requestDTO):
		return [requestDTO.getCurrentRound() / 2]