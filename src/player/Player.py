import sys
sys.path.insert(0, '../api')
from api.ApiPlayerRequestHandler import ApiPlayerRequestHandler

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
        return self.predict(requestDTO)

    def learn(self, learnDTO):
        raise NotImplementedError('subclasses must override learn')
