from __future__ import division

class MyEnvidoScore(object):
    size = 1
    MAX_ENVIDO_SCORE = 33
    def convert(self, requestDTO):
        points = self.getEnvidoScore(requestDTO.getInitialCards())
        return points

    def getEnvidoScore(self, initialCards):
        possibleEnvidos = []
        possibleEnvidos.append(self.envidoFor(initialCards[0], initialCards[1]))
        possibleEnvidos.append(self.envidoFor(initialCards[0], initialCards[2]))
        possibleEnvidos.append(self.envidoFor(initialCards[1], initialCards[2]))
        return [max(possibleEnvidos)/ self.MAX_ENVIDO_SCORE]

    def envidoFor(self, cardOne, cardTwo):
        if(cardOne.suit == cardTwo.suit):
            return 20 + self.cardEnvidoScore(cardOne) + self.cardEnvidoScore(cardTwo)
        else:
            return max([self.cardEnvidoScore(cardOne), self.cardEnvidoScore(cardTwo)])


    def cardEnvidoScore(self, card):
        if(card.value in [10, 11, 12]):
            return 0
        else:
            return card.value
