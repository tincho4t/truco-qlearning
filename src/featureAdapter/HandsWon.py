from SimplifyValueCard import SimplifyValueCard

"""
    Define wich hands are won and loose.
    [On/Off1, Win1, Tie1, Loose1, On/Off2, Win2, Tie2, Loose2]
"""
class HandsWon(object):
    size = 8

    def __init__(self):
        super(HandsWon, self).__init__()
        self.cardConverter = SimplifyValueCard()
    
    def convert(self, requestDTO):
        print requestDTO.rounds
        feature = [0,0,0,0,0,0,0,0]
        rounds = requestDTO.rounds
        for i in range(len(rounds)):
            if self.apply(rounds, i):
                winIndex = self.hoWonIndex(rounds[i])
                feature[2*i] = 1 # On the round
                feature[2*i + winIndex] = 1 # On Win, Tie or Loose bit.
        print "feature: ", feature
        return feature
	
    def apply(self, rounds, i):
        return i < 2 and "opponent_card_played" in rounds[i] and "my_card_played" in rounds[i]

    def hoWonIndex(self, round):
        myCardValue = self.cardConverter.cardToFeature(round["my_card_played"])[0]
        opponetCardValue = self.cardConverter.cardToFeature(round["opponent_card_played"])[0]
        if(myCardValue > opponetCardValue):
            return 1
        elif(myCardValue == opponetCardValue):
            return 2
        else:
            return 3


        