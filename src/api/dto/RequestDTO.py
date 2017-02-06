from Card import Card
from Score import Score
from Round import Round
from Envido import Envido

class RequestDTO(object):
    """ Represent the game state
        that the Request will contain"""
    """ Json example:
        {
            "score": {
                "my_score": 15,
                "opponent_score": 17,
                "score_to_win": 30
            },
            "cards_not_played": [
                {
                    "suit": "gold",
                    "value": 1
                },
                {
                    "suit": "sword",
                    "value": 7
                }
            ],
            "round": {
                "actual_round": "second",
                "first_round": {
                    "my_card_played" : {"suit": "gold", "value": 5},
                    "opponent_card_played": {"suit": "coup", "value": 7}
                },
                "second_round": {
                    "my_card_played" : null,
                    "opponent_card_played": {"suit": "sword", "value": 2}
                }
            },
            "i_am_hand": true,
            "envido": {
                "status": "finished",
                "sung": ["Envido", "Envido", "RealEnvido"],
                "oppenent_envido_score": 26
            }
        }
    """
    def __init__(self, params):
        super(RequestDTO, self).__init__()
        print params
        self.score = Score(params['score'])
        self.cardsNotPlayed = self._cardsNotPlayed(params['cards_not_played'])
        self.round = Round(params['round'])
        self.iAmHand = params['i_am_hand']
        self.envido = Envido(params['envido'])
    
    def _cardsNotPlayed(self, rawCards):
        cards = list()
        for card in rawCards:
            cards.append(Card(card))
        return cards

    def getScore(self):
        return self.score

    def getCardsNotPlayed(self):
        return self.cardsNotPlayed

    def getRound(self):
        return self.round

    def iAmHand(self):
        return self.iAmHand

    def getEnvido(self):
        return self.envido


