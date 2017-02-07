from Player import Player
import sys
sys.path.insert(0, '../featureAdapter')
from featureAdapter.SimplifyMyRemainingCards import SimplifyMyRemainingCards
from featureAdapter.IAmHand import IAmHand


"""Test Player that choose an option randomly"""
class Randomio(Player):
    
    def __init__(self):
        super(Randomio, self).__init__()
        print "RANDOMIO CREADO!!!!"
        self.adapters = [IAmHand(), SimplifyMyRemainingCards()]

    def getAdapters(self):
        return self.adapters
    
    def predict(self, x):
        print "-------> Features: %s" % x
        #TODO: Devolver el response Correcto, devuelvo los Features como debug
        return x
