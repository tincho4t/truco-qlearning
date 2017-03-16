from Player import Player
import sys
sys.path.insert(0, '../featureAdapter')
sys.path.insert(0, '../api')
from featureAdapter.SimplifyMyRemainingCards import SimplifyMyRemainingCards
from featureAdapter.IAmHand import IAmHand
from featureAdapter.RequestDTOFeature import RequestDTOFeature
import random
from api.dto.ActionTakenDTO import ActionTakenDTO
from api.dto.Action import Action


"""Test Player that choose an option randomly"""
class Randomio(Player):
    
    def __init__(self):
        super(Randomio, self).__init__()
        print "RANDOMIO CREADO!!!!"
        self.adapters = [RequestDTOFeature(), IAmHand(), SimplifyMyRemainingCards()]

    def getAdapters(self):
        return self.adapters
    
    def predict(self, x):
        requestDTO = x[0]
        possibleActions = requestDTO.possibleActions
        action = random.choice(possibleActions)
        response = ActionTakenDTO()
        response.setAction(action)
        if(action == Action.PLAYCARD):
            possibleCards = requestDTO.cardsNotPlayed
            print "possibleCards ", possibleCards
            response.setCard(random.choice(possibleCards))
        return response

    def learn(self, learnDTO):
        print "Lerning... ", learnDTO