from Model import Model
import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.exceptions import NotFittedError

# Implementation of a RF addapted for Q Learning
class QLearningRandomForest(Model):
    
    def __init__(self, newEstimatorsPerLearn):
        super(QLearningRandomForest, self).__init__()
        self.newEstimatorsPerLearn = newEstimatorsPerLearn
        self.RF = RandomForestRegressor(warm_start=True, verbose=True, n_estimators=newEstimatorsPerLearn, n_jobs=-1)
    
    def predict(self, X):
        try:
            return self.RF.predict(X) # Vector with estimated points for all actions
        except NotFittedError as e:
            return np.random.rand(15)

    def learn(self, X, ACTION, Y, learnScale = False):
        Y_LEARN = self.getYOnlyForActionTaken(X, ACTION, Y)
        print "TOTAL TREES", self.RF.n_estimators
        self.RF.n_estimators += self.newEstimatorsPerLearn
        self.RF.fit(X, Y_LEARN)

    def getYOnlyForActionTaken(self, X, ACTION, Y):
        predictionRows = list()
        for i in range(X.shape[0]):
            try:
                allActionPredictions = self.RF.predict(X[i,:].reshape(1,-1))[0] # Current predictions
            except NotFittedError as e:
                allActionPredictions = np.random.rand(15)
            allActionPredictions[ACTION[i]] = Y[i] # Only change the prediction for the action that was taken to the expected Y value
            predictionRows += [allActionPredictions]
        return np.array(predictionRows)
