from Model import Model
import numpy as np
from sklearn.exceptions import NotFittedError
from sklearn.neural_network import MLPRegressor

# Implementation of a neural network addapted for Q Learning
class QLearningNeuralNetwork(Model):
    
    def __init__(self, inputLayer, hiddenLayer, outputLayer):
        super(QLearningNeuralNetwork, self).__init__()
        self.NN = MLPRegressor(warm_start=True, verbose=True, max_iter=100000000, tol=0.00000001, batch_size=10)
        self.NN.fit(np.random.rand(100, inputLayer)*0.01,np.random.rand(100, outputLayer)) # Random Initialization of weights

    def predict(self, X):
        return self.NN.predict(np.array(X)) # Vector with estimated points for all actions

    def learn(self, X, ACTION, Y):
        Y_LEARN = self.getYOnlyForActionTaken(X, ACTION, Y)
        self.NN.fit(X, Y_LEARN)

    def getYOnlyForActionTaken(self, X, ACTION, Y):
        predictionRows = list()
        for i in range(X.shape[0]):
            allActionPredictions = self.NN.predict(X[i,:].reshape(1,-1))[0] # FeedForward the current predictions
            allActionPredictions[ACTION[i]] = Y[i] # Only change the prediction for the action that was taken to the expected Y value
            predictionRows += [allActionPredictions]
        return np.array(predictionRows)
