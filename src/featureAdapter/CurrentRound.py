from __future__ import division

class CurrentRound(object):
	size = 3
	def convert(self, requestDTO):
		currentRound = [0,0,0]
		currentRound[requestDTO.getCurrentRound()] = 1
		return currentRound