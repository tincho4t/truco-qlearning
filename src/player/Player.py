import sys
sys.path.insert(0, '../api')
from api.QLearningRequestHandler import QLearningRequestHandler

""" 
    Deveria ser herencia multiple y no heredar asi pero por
    un tema con los constructores por el momento lo deje asi.
"""
class Player(object):
    """Abstract Player"""
    
    """ List of adapters that will transform the requestDTO in features"""
    def getAdapters(self):
        raise NotImplementedError('subclasses must override this method')

    def predict(self):
        raise NotImplementedError('subclasses must override this method')

    def play(self, requestDTO):
        features = list()
        for adapter in self.getAdapters():
            features += adapter.convert(requestDTO)
        return self.predict(features)

    
    def learn(self):
        raise NotImplementedError('subclasses must override learn')
