from Player import Player
import sys
import numpy as np
import tables
sys.path.insert(0, '../featureAdapter')
sys.path.insert(0, '../api')
from featureAdapter.CardUsage import CardUsage
from featureAdapter.CurrentRound import CurrentRound
from featureAdapter.IAmHand import IAmHand
from api.dto.ActionTakenDTO import ActionTakenDTO
from api.dto.Action import Action
from model.QLearningNeuralNetwork import QLearningNeuralNetwork


class QLearner(Player):
    
    def __init__(self):
        super(QLearner, self).__init__()
        print "QLearner created!"
        self.dataFilePath = 'data.h5' # Where to save data for offline learning
        self.adapters = [IAmHand(), CurrentRound(), CardUsage()]
        self.m = self.getFeatureSetSize() # Sum of all adapter sizes
        self.X = np.empty((0,self.m), int) # INPUT of NN (state of game before action)
        self.ACTION = np.empty((0,1), int) # ACTION taken for input X
        self.Y = np.empty((0,1), int) # POINTS given for taking Action in game state (INPUT)
        self.algorithm = QLearningNeuralNetwork()

    def getFeatureSetSize(self):
        m = 0
        for adapter in self.getAdapters():
            m += adapter.size
        return m

    def getCorrectCard(self, action):
        #TODO

    def getPossibleActionsWithCardOrder(self, possibleActions):
        #TODO

    def getAdapters(self):
        return self.adapters

    def getFeatureVector(self, requestDTO):
        featureVector = list()
        for adapter in self.getAdapters():
            featureVector += adapter.convert(requestDTO)
        return featureVector

    def getWinningPossibleAction(self, predictions, possibleActions):
        indexOfSortedPredictions = predictions.argsort()
        possibleActionsWithCardOrder = self.getPossibleActionsWithCardOrder(possibleActions)
        possibleActionsIndexs = [ACTION.getIndex(a) for a in possibleActionsWithCardOrder]
        for index in indexOfSortedPredictions:
            if index in possibleActionsIndexs
                return ACTION.getAction(index)

    def predict(self, requestDTO):
        y_hat_vector = self.algorithm.predict(self.getFeatureVector(requestDTO))
        action = self.getWinningPossibleAction(y_hat_vector, requestDTO.possibleActions)
        response = ActionTakenDTO()
        response.setAction(action)
        if(action in [Action.PLAYCARDLOW, Action.PLAYCARDMIDDLE, Action.PLAYCARDHIGH]):
            response.setCard(self.getCorrectCard(action))
        return response

    def learn(self, learnDTO):
        # We add to our train dataset the game that just ended        
        featureRows = list() # List of game states
        for rDTO in learnDTO.getRequestList():
            featureRows += [self.getFeatureVector(rDTO)]

        actionRows = list() # List of actions
        for action in learnDTO.getActionList():
            actionRows += ACTION.getIndex(action)

        pointsPerState = learnDTO.points/learnDTO.size # Points of game divided equally for each game state that happend in the game
        yRows = np.repeat([pointsPerState], learnDTO.size) # List of points per action taken for each game state
        
        self.X = np.append(self.X, np.array(featureRows), axis = 0)
        self.ACTION = np.append(self.ACTION, np.array(actionRows), axis = 0)
        self.Y = np.append(self.ACTION, yRows, axis = 0)

        if self.learnCondition():
            self.algorithm.learn(self.X, self.ACTION, self.Y) # Really learn from dataset
            self.saveDataset() # Save data for offline learning
            self.clearDataset() # Clear data for new batches

    def learnCondition(self):
        return self.X.shape[0] > 100

    def saveDataset(self):
        f = tables.open_file(dataFile, mode='a')
        # Is this the first time?
        if not "/root/X" in f:
            atom = tables.Int64Atom()
            c_array = f.create_earray(f.root, 'X', atom, (0, self.X.shape[1]))
            c_array = f.create_earray(f.root, 'ACTION', atom, (0, 1))
            c_array = f.create_earray(f.root, 'Y', atom, (0, 1))
        f.root.X.append(self.X)
        f.root.ACTION.append(self.ACTION)
        f.root.Y.append(self.Y)
        f.close()

    def clearDataset(self):
        self.X = np.empty((0,self.m), int) 
        self.ACTION = np.empty((0,1), int)
        self.Y = np.empty((0,1), int)