from Player import Player
import sys
import random
import numpy as np
import tables
sys.path.insert(0, '../featureAdapter')
sys.path.insert(0, '../api')
from featureAdapter.SimplifyValueCard import SimplifyValueCard
from featureAdapter.CardUsage import CardUsage
from featureAdapter.CurrentRound import CurrentRound
from featureAdapter.IAmHand import IAmHand
from featureAdapter.CountPossibleActions import CountPossibleActions
from featureAdapter.RivalCardsUsed import RivalCardsUsed
from featureAdapter.EnvidoAdapter import EnvidoAdapter
from featureAdapter.MyEnvidoScore import MyEnvidoScore
from api.dto.ActionTakenDTO import ActionTakenDTO
from api.dto.Action import Action as ACTION
from api.dto.Card import Card
from model.QLearningNeuralNetwork import QLearningNeuralNetwork
from model.QLearningRandomForest import QLearningRandomForest

class QLearner(Player):
    
    def __init__(self):
        super(QLearner, self).__init__()
        print "QLearner created!"
        self.dataFilePath = 'data.h5' # Where to save data for offline learning
        self.adapters = [IAmHand(), CurrentRound(), CountPossibleActions(), CardUsage(), RivalCardsUsed(), EnvidoAdapter(), MyEnvidoScore()]
        self.m = self.getFeatureSetSize() # Sum of all adapter sizes
        self.X = np.empty((0,self.m), int) # INPUT of NN (state of game before action)
        self.ACTION = np.array([]) # ACTION taken for input X
        self.Y = np.array([]) # POINTS given for taking Action in game state (INPUT)
        self.algorithm = QLearningNeuralNetwork(inputLayer=self.m, hiddenLayerSizes=(100, 100), outputLayer=15)
        #self.algorithm = QLearningRandomForest(newEstimatorsPerLearn=10)
        self.cardConverter = SimplifyValueCard()
        self.lr = 0.8 # LR for reward function
        self.C = 1000 # When to update target algorithm
        self.steps = 0 # Current steps from last update of target algorithm
        self.memorySize = 10000 # Size of memory for ExpRep
        self.trainSize = 1000 # Expe Replay size
        self.epsilon = 0.05 # Probability of taking a random action
        self.loadRandomTestDataset()

    def getFeatureSetSize(self):
        m = 0
        for adapter in self.getAdapters():
            m += adapter.size
        return m

    def actionToCard(self, action, initialCards):
        initialCardValues = [self.cardConverter.cardToFeature(c)[0] for c in initialCards]
        initialCardValuesSortedIndex = np.array(initialCardValues).argsort().reshape(-1)
        if action == ACTION.PLAYCARDLOW:
            return initialCards[initialCardValuesSortedIndex[0]]
        elif action == ACTION.PLAYCARDMIDDLE:
            return initialCards[initialCardValuesSortedIndex[1]]
        else:
            return initialCards[initialCardValuesSortedIndex[2]]

    def cardToAction(self, card, initialCards):
        initialCardValues = [self.cardConverter.cardToFeature(c) for c in initialCards]
        initialCardValuesSortedIndex = np.array(initialCardValues).argsort().reshape(-1)
        if card == initialCards[initialCardValuesSortedIndex[0]]:
            return ACTION.PLAYCARDLOW
        elif card == initialCards[initialCardValuesSortedIndex[1]]:
            return ACTION.PLAYCARDMIDDLE
        else:
            return ACTION.PLAYCARDHIGH

    def getCardActionsAvailable(self, initialCards, cardsNotPlayed):
        initialCardValues = [self.cardConverter.cardToFeature(c)[0] for c in initialCards]
        initialCardValuesSortedIndex = np.array(initialCardValues).argsort().reshape(-1)
        possibleCardActions = list()
        if initialCards[initialCardValuesSortedIndex[0]] in cardsNotPlayed:
            possibleCardActions += [ACTION.PLAYCARDLOW]
        if initialCards[initialCardValuesSortedIndex[1]] in cardsNotPlayed:
            possibleCardActions += [ACTION.PLAYCARDMIDDLE]
        if initialCards[initialCardValuesSortedIndex[2]] in cardsNotPlayed:
            possibleCardActions += [ACTION.PLAYCARDHIGH]
        return possibleCardActions


    def getPossibleActionsWithCardOrder(self, requestDTO):
        possibleActions = list()
        # Is playcard an action available
        if ACTION.PLAYCARD in requestDTO.possibleActions:
            cardActionsAvailable = self.getCardActionsAvailable(requestDTO.initialCards, requestDTO.cardsNotPlayed)
            possibleActions += cardActionsAvailable
        for action in requestDTO.possibleActions:
            if not action == ACTION.PLAYCARD:
                possibleActions += [action]
        return possibleActions

    def getAdapters(self):
        return self.adapters

    def getFeatureVector(self, requestDTO):
        featureVector = list()
        for adapter in self.getAdapters():
            featureVector += adapter.convert(requestDTO)
        return featureVector

    def getPossibleActionIndexes(self, requestDTO):
        possibleActionsWithCardOrder = self.getPossibleActionsWithCardOrder(requestDTO)
        return [ACTION.actionToIndexDic[a] for a in possibleActionsWithCardOrder]

    def getWinningPossibleAction(self, predictions, requestDTO):
        possibleActionsIndexs = self.getPossibleActionIndexes(requestDTO)
        return self.getWinnerAction(predictions, possibleActionsIndexs)
    
    def getWinnerAction(self, predictions, possibleActionsIndexs):
        indexOfSortedPredictions = predictions[0].argsort()[::-1] # Reversed sorted indexes
        for index in indexOfSortedPredictions:
            if index in possibleActionsIndexs:
                return ACTION.actionToStringDic[index]

    def predict(self, requestDTO):
        if(self.chooseRandomOption()):
            return self.getRandomOption(requestDTO)

        yHatVector = self.algorithm.predict(self.getFeatureVector(requestDTO))
        action = self.getWinningPossibleAction(yHatVector, requestDTO)
        response = ActionTakenDTO()
        if(action in [ACTION.PLAYCARDLOW, ACTION.PLAYCARDMIDDLE, ACTION.PLAYCARDHIGH]):
            response.setCard(self.actionToCard(action, requestDTO.initialCards))
            action = ACTION.PLAYCARD
        response.setAction(action)
        return response

    def learn(self, learnDTO):
        # We add to our train dataset the game that just ended        
        featureRows = list() # List of game states
        possibleActionsRows = list() # Fixed List of possible action indexes
        requestList = learnDTO.getGameStatusList()
        actionList = learnDTO.getActionList()
        for rDTO in requestList:
            featureRows += [self.getFeatureVector(rDTO)]
            possibleActionsRows.append(self.fixedPossibleActions(rDTO))

        actionRows = list() # List of actions
        for i in range(len(actionList)):
            actionDic = actionList[i]
            action = actionDic['action']
            if action == ACTION.PLAYCARD:
                action = self.cardToAction(Card(actionDic['card']), requestList[i].initialCards)
            actionRows += [ACTION.actionToIndexDic[action]]

        yRows = list() # List of rewards to learn
        for row in featureRows[1:]:
            # Rj + y * max(Q for all actions of next state [1:])
            # Target network hack
            yRows.append(0 + self.lr*max(self.algorithm.predict(row, target=True)[0]))
        yRows.append(learnDTO.points) # Last action take got the points of the game

        # Experience Replay hack
        self.X = np.append(featureRows, self.X, axis = 0)
        self.ACTION = np.append(actionRows, self.ACTION, axis = 0)
        self.Y = np.append(yRows, self.Y, axis = 0)
        if self.Y.shape[0] > self.memorySize:
            diff = self.Y.shape[0] - self.memorySize
            self.X = self.X[:-diff]
            self.ACTION = self.ACTION[:-diff]
            self.Y = self.Y[:-diff]
        if self.steps % 100 == 0:
            randomTrainIndexes = np.random.randint(0, min(self.memorySize, self.Y.shape[0]), self.trainSize)
            self.algorithm.learn(self.X[randomTrainIndexes,:], self.ACTION[randomTrainIndexes], self.Y[randomTrainIndexes])
            #self.saveDataset(np.array(featureRows), np.array(actionRows), np.array(yRows), np.array(possibleActionsRows)) # Save data for offline learning

        # Target network hack
        self.steps += 1
        if self.C < self.steps:
            self.algorithm.updateTarget()
            self.steps = 0
            self.testConvergence()

        return "OK"

    def saveDataset(self, X, ACTION, Y, POSSIBLE_ACTIONS):
        f = tables.open_file(self.dataFilePath, mode='a')
        # Is this the first time?
        if not "/X" in f:
            atom = tables.Int64Atom()
            atomFloat = tables.Float64Atom()
            c_array = f.create_earray(f.root, 'X', atomFloat, (0, X.shape[1]))
            c_array = f.create_earray(f.root, 'ACTION', atom, (0, 1))
            c_array = f.create_earray(f.root, 'Y', atomFloat, (0, 1))
            c_array = f.create_earray(f.root, 'POSSIBLE_ACTIONS', atomFloat, (0, POSSIBLE_ACTIONS.shape[1]))
        f.root.X.append(X)
        f.root.ACTION.append(ACTION.reshape(-1, 1))
        f.root.Y.append(Y.reshape(-1, 1))
        f.root.POSSIBLE_ACTIONS.append(POSSIBLE_ACTIONS)
        f.close()

    def clearDataset(self):
        self.X = np.empty((0,self.m), int)
        self.ACTION = np.array([])
        self.Y = np.array([])

    def getRandomOption(self, requestDTO):
        action = random.choice(requestDTO.possibleActions)
        response = ActionTakenDTO()
        response.setAction(action)
        if(action == ACTION.PLAYCARD):
            possibleCards = requestDTO.cardsNotPlayed
            response.setCard(random.choice(possibleCards))
        return response

    def chooseRandomOption(self):
        return random.random() < self.epsilon


    #################### TEST CONVERGENCE SECTION ###################
    def testConvergence(self):
        newPredictions = self.algorithm.predict(self.testDataset, target=True)
        actionsPredicted = list()
        for i in range(newPredictions.shape[0]):
            p = newPredictions[i]
            actionsPredicted.append(self.getWinnerAction([p], self.testDatasetPossibleActions[i]))
        actionsPredicted = np.array(actionsPredicted)
        print "Porcentaje de cambios", 100 * np.mean(self.lastPredictions != actionsPredicted),"%"
        self.lastPredictions = actionsPredicted

    def loadRandomTestDataset(self):
        f = tables.open_file("random_test_convergence.h5")
        self.testDataset = np.array(f.root.X)
        
        self.testDatasetPossibleActions = list()
        for possibleActions in np.array(f.root.POSSIBLE_ACTIONS):
            indexes = np.where(possibleActions)[0]
            # self.testDatasetPossibleActions.append([ACTION.actionToStringDic[i] for i in indexes])
            self.testDatasetPossibleActions.append(indexes)
        self.testDatasetPossibleActions = np.array(self.testDatasetPossibleActions)

        self.lastPredictions = np.zeros(self.testDataset.shape[0])
        f.close()

    def fixedPossibleActions(self, requestDTO):
        actions = np.zeros(len(ACTION.actionToIndexDic))
        possibleActionsIndexs = self.getPossibleActionIndexes(requestDTO)
        for index in possibleActionsIndexs:
            actions[index] = 1
        return actions

    #################################################################