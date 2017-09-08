from api.dto.Card import Card
from SimplifyValueCard import SimplifyValueCard
"""
    Compara la carta acual que jugo el oponente contra las mias
    y te indica si [Win, Tie, Loose].
"""
class CompareCardsToOpponentsPlayedCard(object):
    size = 10 # 1 hay carta del oponente + [win, tie, loose] x3

    def __init__(self):
        super(CompareCardsToOpponentsPlayedCard, self).__init__()
        self.cardConverter = SimplifyValueCard()

    def convert(self, requestDTO):
        feature = [0,0,0,0,0,0,0,0,0,0]
        currentRound = requestDTO.rounds[requestDTO.getCurrentRound()]
        if("opponent_card_played" in currentRound):
            opponentsCardPlayed = Card(currentRound["opponent_card_played"])
            feature[0] = 1 # On opponent Card
            initialCards = requestDTO.getInitialCards()
            for i in range(3):
                myCard = initialCards[i]
                winIndex = self.hoWonIndex(myCard, opponentsCardPlayed)
                feature[1 + 3*i + winIndex] = 1 # On Win, Tie or Loose bit.
        return feature


    def hoWonIndex(self, myCard, opponetCard):
        myCardValue = self.cardConverter.cardToFeature(myCard)[0]
        opponetCardValue = self.cardConverter.cardToFeature(opponetCard)[0]
        if(myCardValue > opponetCardValue):
            return 0
        elif(myCardValue == opponetCardValue):
            return 1
        else:
            return 2










