import sys
sys.path.insert(0, '../api')
from api.QLearningRequestHandler import QLearningRequestHandler

""" 
    Deveria ser herencia multiple y no heredar asi pero por
    un tema con los constructores por el momento lo deje asi.
"""
class Player(QLearningRequestHandler):
    """Abstract Player"""
    
    def play(self, x):
        pass
        raise NotImplementedError('subclasses must override play')
    
    def learn(self):
        pass
        raise NotImplementedError('subclasses must override learn')
