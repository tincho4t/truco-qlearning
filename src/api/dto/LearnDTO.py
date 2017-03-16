import sys
sys.path.insert(0, '../api')

from api.dto.GameStatusDTO import GameStatusDTO

class LearnDTO(object):
	"""docstring for LearnDTO"""
	def __init__(self, dic):
		super(LearnDTO, self).__init__()
		self.gameStatusList = []
		self.actionList = []
		for row in dic['hand_hystory']:
			self.gameStatusList.append(GameStatusDTO(row['gameStatus']))
			self.actionList.append(row['action'])
		self.size = len(self.gameStatusList)
		self.points = dic['points']

	def getActionList(self):
		return self.actionList

	def getGameStatusList(self):
		return self.gameStatusList
