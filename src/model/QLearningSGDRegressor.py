from Model import Model
import numpy as np
from sklearn.base import clone
from copy import deepcopy
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.exceptions import NotFittedError
from api.dto.Action import Action as ACTION

# Implementation of a SGDRegressor addapted for Q Learning
class QLearningSGDRegressor(Model):
    
    def __init__(self):
        super(QLearningSGDRegressor, self).__init__()
        self.Q = MultiOutputRegressor(SGDRegressor(warm_start=True, verbose=0, learning_rate='constant', eta0=0.0001), n_jobs=1)
        self.QTarget = clone(self.Q)
    
    def predict(self, X, target=False):
        try:
            if target:
                return self.QTarget.predict(X)
            else:
                return self.Q.predict(X) # Vector with estimated points for all actions
        except NotFittedError as e:
            return np.random.rand(1, 15)

    def updateTarget(self):
        print("TARGET UPDATED")
        self.QTarget = deepcopy(self.Q)

    def learn(self, X, ACTION, Y, learnScale = False):
        Y_LEARN = self.getYOnlyForActionTaken(X, ACTION, Y)
        self.Q.fit(X, Y_LEARN)

    def getYOnlyForActionTaken(self, X, ACTION, Y):
        predictionRows = list()
        for i in range(X.shape[0]):
            try:
                allActionPredictions = self.Q.predict(X[i,:].reshape(1,-1))[0] # FeedForward the current predictions
            except NotFittedError as e:
                allActionPredictions = np.random.rand(15)
            if np.random.rand(1) < 0.01:
                print(ACTION[i],allActionPredictions[ACTION[i]], Y[i])
            allActionPredictions[ACTION[i]] = Y[i] # Only change the prediction for the action that was taken to the expected Y value
            predictionRows += [allActionPredictions]
        return np.array(predictionRows)