from SimplifyValueCard import SimplifyValueCard

"""
    Convert the cards not played yet into 4 options values.
    4,5,6,7                -> 1
    10,11,12,Anchos falsos -> 2
    2,3                    -> 3
    Los 7 y Anchos         -> 4
"""
class SimplifyMyRemainingCards(SimplifyValueCard):
    
    def convert(self, requestDTO):
        feature = list()
        cards = requestDTO.getCardsNotPlayed()
        for card in cards:
            feature += self.cardToFeature(card)
        return feature
