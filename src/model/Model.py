
class Model(object):
    """Abstract Model"""
    
    def predict(self, X):
        raise NotImplementedError('subclasses must override this method')

    def learn(self, learnDTO):
        raise NotImplementedError('subclasses must override learn')
