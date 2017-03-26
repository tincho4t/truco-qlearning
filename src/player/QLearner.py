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
from api.dto.ActionTakenDTO import ActionTakenDTO
from api.dto.Action import Action as ACTION
from api.dto.Card import Card
from model.QLearningNeuralNetwork import QLearningNeuralNetwork

class QLearner(Player):
    
    def __init__(self):
        super(QLearner, self).__init__()
        print "QLearner created!"
        self.dataFilePath = 'data.h5' # Where to save data for offline learning
        self.adapters = [IAmHand(), CurrentRound(), CountPossibleActions(), CardUsage(), RivalCardsUsed(), EnvidoAdapter()]
        self.m = self.getFeatureSetSize() # Sum of all adapter sizes
        self.X = np.empty((0,self.m), int) # INPUT of NN (state of game before action)
        self.ACTION = np.array([]) # ACTION taken for input X
        self.Y = np.array([]) # POINTS given for taking Action in game state (INPUT)
        self.algorithm = QLearningNeuralNetwork(inputLayer=self.m, hiddenLayer=1000, outputLayer=15)
        self.cardConverter = SimplifyValueCard()
        self.learningLoops = 0

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

    def getWinningPossibleAction(self, predictions, possibleActions):
        indexOfSortedPredictions = predictions[0].argsort()[::-1] # Reversed sorted indexes
        possibleActionsWithCardOrder = self.getPossibleActionsWithCardOrder(possibleActions)
        possibleActionsIndexs = [ACTION.actionToIndexDic[a] for a in possibleActionsWithCardOrder]
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
        requestList = learnDTO.getGameStatusList()
        actionList = learnDTO.getActionList()
        for rDTO in requestList:
            featureRows += [self.getFeatureVector(rDTO)]

        actionRows = list() # List of actions
        for i in range(len(actionList)):
            actionDic = actionList[i]
            action = actionDic['action']
            if action == ACTION.PLAYCARD:
                action = self.cardToAction(Card(actionDic['card']), requestList[i].initialCards)
            actionRows += [ACTION.actionToIndexDic[action]]

        pointsPerState = learnDTO.points/learnDTO.size # Points of game divided equally for each game state that happend in the game
        yRows = np.repeat([pointsPerState], learnDTO.size) # List of points per action taken for each game state

        self.X = np.append(self.X, np.array(featureRows), axis = 0)
        self.ACTION = np.append(self.ACTION, np.array(actionRows), axis = 0)
        self.Y = np.append(self.Y, yRows, axis = 0)

        self.learningLoops += 1
        if self.learnCondition():
            self.algorithm.learn(self.X, self.ACTION, self.Y, learnScale=(self.X.shape[0] > 500)) # Really learn from dataset
            self.saveDataset() # Save data for offline learning
            self.clearDataset() # Clear data for new batches
        return "OK"

    def learnCondition(self):
        print self.X.shape[0]
        return self.X.shape[0] > 100

    def saveDataset(self):
        f = tables.open_file(self.dataFilePath, mode='a')
        # Is this the first time?
        if not "/X" in f:
            atom = tables.Int64Atom()
            atomFloat = tables.Float64Atom()
            c_array = f.create_earray(f.root, 'X', atomFloat, (0, self.X.shape[1]))
            c_array = f.create_earray(f.root, 'ACTION', atom, (0, 1))
            c_array = f.create_earray(f.root, 'Y', atomFloat, (0, 1))
        f.root.X.append(self.X)
        f.root.ACTION.append(self.ACTION.reshape(-1, 1))
        f.root.Y.append(self.Y.reshape(-1, 1))
        f.close()

    def clearDataset(self):
        self.X = np.empty((0,self.m), int)
        self.ACTION = np.array([])
        self.Y = np.array([])


    def getRandomOption(self, requestDTO):
        print "taking random option"
        action = random.choice(requestDTO.possibleActions)
        response = ActionTakenDTO()
        response.setAction(action)
        if(action == ACTION.PLAYCARD):
            possibleCards = requestDTO.cardsNotPlayed
            response.setCard(random.choice(possibleCards))
        return response

    def chooseRandomOption(self):
        MAX_RANDOM_ITERATIONS = 50000
        if(self.learningLoops >= MAX_RANDOM_ITERATIONS):
            return False
        else:
            probability = 1 - (self.learningLoops / MAX_RANDOM_ITERATIONS)
            return random.random() < probability
