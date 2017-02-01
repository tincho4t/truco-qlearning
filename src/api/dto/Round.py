
class Round(object):
    """Represent the state of the round.
    Example:
        {
            actual_round = "second",
            first_round: {
                my_card_played : ...
                opponent_card_played: ...
            },
            second_round: {
                my_card_played : ...
                opponent_card_played: ...
            }
        }
    """
    def __init__(self, dic):
        super(Round, self).__init__()
        self.actualRound = dic['actual_round']
        self.setFirstRound = self.convertToRound(dic.get('first_round',None))
        self.setSecondRound = self.convertToRound(dic.get('second_round',None))
        self.setThridRound = self.convertToRound(dic.get('third_round',None))

    def convertToRound(self, jsonRound):
        round = None
        if(jsonRound):
            round = {
                'my_card_played': jsonRound['my_card_played'],
                'opponent_card_played': jsonRound['opponent_card_played']
            }
        return round