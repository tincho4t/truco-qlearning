from SimplifyValueCard import SimplifyValueCard
import sys
sys.path.insert(0, '../api')
from api.dto.Card import Card
"""
    Convert the Rival cards played as [AVAILABLE_1, VALUE_1, ...].
"""
class RivalCardsUsed(object):
    size = 6
    def convert(self, requestDTO):
        feature = [0,0,0,0,0,0]
        cardConverter = SimplifyValueCard()
        rounds = requestDTO.rounds
        for i in range(len(rounds)):
            if "opponent_card_played" in rounds[i]:
                card = Card(rounds[i]["opponent_card_played"])
                feature[2*i] = 1
                feature[2*i +1] = cardConverter.cardToFeature(card)[0]
        return feature