from Model import Model
from sklearn.neural_network import MLPClassifier

# Implementation of a neural network addapted for Q Learning
class QLearningNeuralNetwork(Model):
    
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.NN = MLPClassifier(warm_start=True)

    def predict(self, X):
    	return self.NN.predict_proba(X) # Vector with estimated points for all actions

    def learn(self, X, ACTION, Y):
    	Y_LEARN = self.getYOnlyForActions(X, ACTION, Y)
    	self.NN.fit(X, Y_LEARN)

    def getYOnlyForActionTaken(self, X, ACTION, Y):
    	predictionRows = list()
    	for i in range(X.shape[0]):
    		allActionPredictions = self.NN.predict_proba(X[i,:]) # FeedForward the current predictions
    		allActionPredictions[ACTION[i]] = Y[i] # Only change the prediction for the action that was taken to the expected Y value
    		predictionRows += [allActionPredictions]
    	return np.array(predictionRows)
