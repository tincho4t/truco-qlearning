from SimplifyValueCard import SimplifyValueCard
import sys
sys.path.insert(0, '../api')
from api.dto.Card import Card
"""
    Convert the cards not played yet into 4 options values.
    4,5,6,7                -> 1
    10,11,12,Anchos falsos -> 2
    2,3                    -> 3
    Los 7 y Anchos         -> 4
    +
    Add a bit of available or not
"""
class RivalCardsUsed(object):
    size = 3
    def convert(self, requestDTO):
        feature = [-1,-1,-1]
        cardConverter = SimplifyValueCard()
        rounds = requestDTO.rounds
        for i in range(len(rounds)):
            if "opponent_card_played" in rounds[i]:
                card = Card(rounds[i]["opponent_card_played"])
                feature[i] = cardConverter.cardToFeature(card)[0]
        return feature