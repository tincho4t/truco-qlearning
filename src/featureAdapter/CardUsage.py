"""
    Convert the cards not played yet into 4 options values.
    4,5,6,7                -> 1
    10,11,12,Anchos falsos -> 2
    2,3                    -> 3
    Los 7 y Anchos         -> 4
    +
    Add a bit of available or not
"""
class CardUsage(object):
    
    def convert(self, requestDTO):
        feature = list()
        cardsNotPlayed = requestDTO.getCardsNotPlayed()
        initialCards = requestDTO.getInitialCards()
        for card in initialCards:
            feature += [self.cardToFeature(card), (card in cardsNotPlayed)] #Card + 0 or 1 if it is available or not
        return feature