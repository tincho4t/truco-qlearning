from api.dto.Action import Action as ACTION

class CountPossibleActions(object):
    size = 1
    def convert(self, requestDTO):
        return [len(requestDTO.possibleActions) / ACTION.POSSIBLE_ACTIONS]