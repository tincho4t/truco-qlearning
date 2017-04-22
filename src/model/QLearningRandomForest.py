from Model import Model
import numpy as np
from sklearn.base import clone
from copy import deepcopy
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.exceptions import NotFittedError

# Implementation of a RF addapted for Q Learning
class QLearningRandomForest(Model):
    
    def __init__(self, newEstimatorsPerLearn):
        super(QLearningRandomForest, self).__init__()
        self.newEstimatorsPerLearn = newEstimatorsPerLearn
        self.Q = RandomForestRegressor(warm_start=True, n_estimators=newEstimatorsPerLearn, n_jobs=1)
        self.QTarget = clone(self.Q)

    def predict(self, X, target=False):
        try:
            if target:
                return self.QTarget.predict(X)
            else:
                return self.Q.predict(X) # Vector with estimated points for all actions
        except NotFittedError as e:
            return np.random.rand(1, 15)

    def learn(self, X, ACTION, Y, learnScale = False):
        Y_LEARN = self.getYOnlyForActionTaken(X, ACTION, Y)
        print "TOTAL TREES", self.Q.n_estimators
        self.Q.n_estimators += self.newEstimatorsPerLearn
        self.Q.fit(X, Y_LEARN)

    def updateTarget(self):
        print("TARGET UPDATED")
        self.QTarget = deepcopy(self.Q)

    def getYOnlyForActionTaken(self, X, ACTION, Y):
        predictionRows = list()
        for i in range(X.shape[0]):
            try:
                allActionPredictions = self.Q.predict(X[i,:].reshape(1,-1))[0] # Current predictions
            except NotFittedError as e:
                allActionPredictions = np.random.rand(15)
            allActionPredictions[ACTION[i]] = Y[i] # Only change the prediction for the action that was taken to the expected Y value
            predictionRows += [allActionPredictions]
        return np.array(predictionRows)
