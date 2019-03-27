from SimplifyValueCard import SimplifyValueCard
from api.dto.Action import Action as ACTION
import numpy as np

class PossibleActionsBitMap(object):
    size = ACTION.POSSIBLE_ACTIONS
    cardConverter = SimplifyValueCard()

    def convert(self, requestDTO):
    	bitmap = [0] * ACTION.POSSIBLE_ACTIONS
    	for action in requestDTO.possibleActions:
    		if action == ACTION.PLAYCARD:
    			for playcardAction in self.getPossibleCardActions(requestDTO):
    				self.turnOn(bitmap, playcardAction)
    		else:
    			self.turnOn(bitmap,action)
        return bitmap

    def turnOn(self, bitmap, action):
    	bitmap[ACTION.actionToIndexDic[action]] = 1

    def getPossibleCardActions(self, requestDTO):
        return self.getCardActionsAvailable(requestDTO.initialCards, requestDTO.cardsNotPlayed)

    def getCardActionsAvailable(self, initialCards, cardsNotPlayed):
        initialCardValues = [self.cardConverter.cardToFeature(c)[0] for c in initialCards]
        initialCardValuesSortedIndex = np.array(initialCardValues).argsort().reshape(-1)
        possibleCardActions = list()
        if initialCards[initialCardValuesSortedIndex[0]] in cardsNotPlayed:
            possibleCardActions += [ACTION.PLAYCARDLOW]
        if initialCards[initialCardValuesSortedIndex[1]] in cardsNotPlayed:
            possibleCardActions += [ACTION.PLAYCARDMIDDLE]
        if initialCards[initialCardValuesSortedIndex[2]] in cardsNotPlayed:
            possibleCardActions += [ACTION.PLAYCARDHIGH]
        return possibleCardActions