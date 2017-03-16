from Model import Model
import numpy as np
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.exceptions import NotFittedError

# Implementation of a neural network addapted for Q Learning
class QLearningNeuralNetwork(Model):
    
    def __init__(self, inputLayer, hiddenLayer, outputLayer):
        super(QLearningNeuralNetwork, self).__init__()
        self.NN = MLPRegressor(warm_start=True, verbose=True, max_iter=100000000, tol=0.00000001, batch_size=10)
        self.outputLayer = outputLayer
        self.Scaler = preprocessing.StandardScaler()

    def predict(self, X):
        try:
            if False:
                X = self.Scaler.transform(np.array(X))
            return self.NN.predict(X) # Vector with estimated points for all actions
        except NotFittedError as e:
            print("First iteration")
            return np.random.rand(1, self.outputLayer)

    def learn(self, X, ACTION, Y, learnScale = False):
        Y_LEARN = self.getYOnlyForActionTaken(X, ACTION, Y)
        if False:
            self.Scaler = self.Scaler.fit(X)    
            X = self.Scaler.transform(X)
        print X
        self.NN.fit(X, Y_LEARN)

    def getYOnlyForActionTaken(self, X, ACTION, Y):
        predictionRows = list()
        for i in range(X.shape[0]):
            try:
                allActionPredictions = self.NN.predict(X[i,:].reshape(1,-1))[0] # FeedForward the current predictions
            except NotFittedError as e:
                allActionPredictions = np.random.rand(self.outputLayer)
            allActionPredictions[ACTION[i]] = Y[i] # Only change the prediction for the action that was taken to the expected Y value
            predictionRows += [allActionPredictions]
        return np.array(predictionRows)
