from __future__ import division
from FeatureAdapterInterface import FeatureAdapterInterface
import sys
sys.path.insert(0, '../api/dto')
from api.dto.Suit import Suit

class SimplifyValueCard(FeatureAdapterInterface):
    """Abstract class that contains the logic to convert the 
       cards into 0 to 14 options values.
    """
    FIXED_VALUES = {
        4: 0,
        5: 1,
        6: 2,
       #7: 3,  
        10: 4,
        11: 5,
        12: 6,
       #1: 7.
        2: 8,
        3: 9 
    }

    def cardToFeature(self, card):
        return [self.cardValue(card) / 13]

    def cardValue(self, card):
        if(card.value in self.FIXED_VALUES.keys()):
            return self.FIXED_VALUES.get(card.value)
        elif(card.value == 7 and card.suit in [Suit.COUP, Suit.CLUB]):
            return 3
        elif(card.value == 1 and card.suit in [Suit.COUP, Suit.COIN]):
            return 7
        elif(card.value == 7 and card.suit == Suit.COIN):
            return 10
        elif(card.value == 7 and card.suit == Suit.SWORD):
            return 11
        elif(card.value == 1 and card.suit == Suit.CLUB):
            return 12        
        else:
            return 13
