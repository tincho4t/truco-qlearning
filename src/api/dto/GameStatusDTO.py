from Card import Card
from Score import Score
from Envido import Envido

class GameStatusDTO(object):
    """ Represent the game state
        that the Request will contain"""
    """ Json example:
        {
            "score": {
                "my_score": 15,
                "opponent_score": 17,
                "score_to_win": 30
            },
            "initial_cards": [
                {
                    "suit": "gold",
                    "value": 1
                },
                {
                    "suit": "sword",
                    "value": 7
                },
                {
                    "suit": "cup",
                    "value": 12
                }
            ],            
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
            "current_round": 1, // "Second"
            "rounds": [
                {
                    "my_card_played" : {"suit": "gold", "value": 5},
                    "opponent_card_played": {"suit": "coup", "value": 7}
                },
                {
                    "my_card_played" : null,
                    "opponent_card_played": {"suit": "sword", "value": 2}
                }
            ],
            "i_am_hand": true,
            "envido": {
                "is_open": false,
                "sung": ["Envido", "Envido", "RealEnvido"],
                "oppenent_envido_score": 26
            },
            "possible_actions": ["Truco", "PlayCard"]
        }
    """
    def __init__(self, params):
        super(GameStatusDTO, self).__init__()
        print params
        self.score = Score(params['score'])
        self.cardsNotPlayed = self._cardsNotPlayed(params['cards_not_played'])
        self.initialCards = self._initialCards(params['initial_cards'])
        self.currentRound = params['current_round']
        self.rounds = params['rounds']
        self.iAmHand = params['i_am_hand']
        self.envido = Envido(params['envido'])
        if('possible_actions' in params):
            self.possibleActions = params['possible_actions']
    
    def _cardsNotPlayed(self, rawCards):
        cards = list()
        for card in rawCards:
            cards.append(Card(card))
        return cards

    def _initialCards(self, rawCards):
        cards = list()
        for card in rawCards:
            cards.append(Card(card))
        return cards

    def getScore(self):
        return self.score

    def getCardsNotPlayed(self):
        return self.cardsNotPlayed

    def getInitialCards(self):
        return self.initialCards    

    def getRounds(self):
        return self.rounds

    def getCurrentRound(self):
        return self.currentRound

    def getEnvido(self):
        return self.envido

