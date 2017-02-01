

class Score(object):
	
	def __init__(self, dic):
		super(Score, self).__init__()
		self.myScore = dic['my_score']
		self.opponentScore = dic['opponent_score']
		self.scoreToWin = dic['score_to_win']

		