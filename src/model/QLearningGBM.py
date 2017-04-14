from Model import Model
import numpy as np
from sklearn import preprocessing
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.exceptions import NotFittedError

# Implementation of a GBM addapted for Q Learning
class QLearningGBM(Model):
    
    def __init__(self, newEstimatorsPerLearn):
        super(QLearningGBM, self).__init__()
        self.newEstimatorsPerLearn = newEstimatorsPerLearn
        self.GBM = MultiOutputRegressor(GradientBoostingRegressor(warm_start=True, verbose=True, n_estimators=newEstimatorsPerLearn, learning_rate=0.01), n_jobs=-1)
    
    def predict(self, X):
        try:
            return self.GBM.predict(X) # Vector with estimated points for all actions
        except NotFittedError as e:
            return np.random.rand(15)

    def learn(self, X, ACTION, Y, learnScale = False):
        Y_LEARN = self.getYOnlyForActionTaken(X, ACTION, Y)
        self.GBM.estimator.n_estimators += self.newEstimatorsPerLearn
        print "TOTAL TREES", self.GBM.estimator.n_estimators
        self.GBM.fit(X, Y_LEARN)

    def getYOnlyForActionTaken(self, X, ACTION, Y):
        predictionRows = list()
        for i in range(X.shape[0]):
            try:
                allActionPredictions = self.GBM.predict(X[i,:].reshape(1,-1))[0] # Current predictions
            except NotFittedError as e:
                allActionPredictions = np.random.rand(15)
            allActionPredictions[ACTION[i]] = Y[i] # Only change the prediction for the action that was taken to the expected Y value
            predictionRows += [allActionPredictions]
        return np.array(predictionRows)