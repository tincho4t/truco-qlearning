
class CountPossibleActions(object):
    size = 1
    def convert(self, requestDTO):
        return [len(requestDTO.possibleActions) / 15.0]