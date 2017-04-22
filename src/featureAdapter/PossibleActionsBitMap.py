from api.dto.Action import Action as ACTION

class PossibleActionsBitMap(object):
    size = 15
    def convert(self, requestDTO):
    	bitmap = [0] * 15
    	for action in requestDTO.possibleActions:
    		bitmap[ACTION.actionToIndexDic[action]] = 1
        return bitmap