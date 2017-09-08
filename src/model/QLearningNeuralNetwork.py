from sklearn.externals import joblib
from Model import Model
import numpy as np
from sklearn.base import clone
from copy import deepcopy
from sklearn.neural_network import MLPRegressor
from sklearn.exceptions import NotFittedError

# Implementation of a neural network addapted for Q Learning
class QLearningNeuralNetwork(Model):
    
    def __init__(self, inputLayer, hiddenLayerSizes, outputLayer, existingAlgoPath=None):
        super(QLearningNeuralNetwork, self).__init__()
        self.lr_drop_rate = 0.995
        if existingAlgoPath is None:
            self.Q = MLPRegressor(warm_start=True, max_iter=5, verbose=0, tol=-1, solver='sgd', alpha=0.001 ,learning_rate_init=0.00035, learning_rate='constant', batch_size=32, hidden_layer_sizes=hiddenLayerSizes)
            self.QTarget = clone(self.Q)
        else:
            self.Q = joblib.load(existingAlgoPath+"_Q.pkl")
            self.QTarget = joblib.load(existingAlgoPath+"_QTarget.pkl")
        self.outputLayer = outputLayer

    
    def predict(self, X, target=False):
        try:
            if target:
                return self.QTarget.predict(X)
            else:
                return self.Q.predict(X) # Vector with estimated points for all actions
        except NotFittedError as e:
            return np.random.rand(1, self.outputLayer)

    def updateLR(self):
        if self.Q.learning_rate_init > 0.00001:
            self.Q.learning_rate_init*=self.lr_drop_rate
    
    def updateTarget(self):
        print("TARGET UPDATED")
        self.QTarget = deepcopy(self.Q)
        print("Current LR is",self.Q.learning_rate_init)
    
    def learn(self, X, ACTION, Y, learnScale = False):
        Y_LEARN = self.getYOnlyForActionTaken(X, ACTION, Y)
        self.Q = self.Q.fit(X, Y_LEARN)
    
    def getYOnlyForActionTaken(self, X, ACTION, Y):
        predictionRows = list()
        for i in range(X.shape[0]):
            try:
                allActionPredictions = self.Q.predict(X[i,:].reshape(1,-1))[0] # FeedForward the current predictions
            except NotFittedError as e:
                allActionPredictions = np.random.rand(self.outputLayer)
            allActionPredictions[int(ACTION[i])] = Y[i] # Only change the prediction for the action that was taken to the expected Y value
            predictionRows += [allActionPredictions]
        return np.array(predictionRows)
