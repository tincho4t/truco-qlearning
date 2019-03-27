import os
from sklearn.externals import joblib
from Player import Player
import math
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
from featureAdapter.CompareCardsToOpponentsPlayedCard import CompareCardsToOpponentsPlayedCard
from featureAdapter.ScoreFeature import ScoreFeature
from featureAdapter.TrucoLevel import TrucoLevel
from featureAdapter.PossibleActionsBitMap import PossibleActionsBitMap
from featureAdapter.HandsWon import HandsWon
from featureAdapter.DesicionType import DesicionType
from api.dto.ActionTakenDTO import ActionTakenDTO
from api.dto.Action import Action as ACTION
from api.dto.Card import Card
from model.QLearningNeuralNetwork import QLearningNeuralNetwork
from model.QLearningTensorflow import QLearningTensorflow

AUDIT_ACTIONS = ["Truco", "ReTruco", "ValeCuatro", "Quiero", "NoQuiero", "Envido", "RealEnvido", "FaltaEnvido", "PlayCardLow", "PlayCardMiddle", "PlayCardHigh"]
AUDIT_DIC = {
            "ENVIDO_ALTO_SOY_MANO": [0.23076923076923078, True, 0.3076923076923077, True, 0.6923076923076923, True, 1, 0, 0, 1, 0.3333333333333333, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0.9090909090909091, 0.0, 0.0, 0.0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "ENVIDO_MEDIO_SOY_MANO": [0.15384615384615385, True, 0.3076923076923077, True, 0.38461538461538464, True, 1, 0, 0, 1, 0.3333333333333333, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0.7878787878787878, 0.0, 0.0, 0.0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "JUGAR_BAJA_MEJOR_OPCION": [0.3076923076923077, True, 0.46153846153846156, True, 0.6923076923076923, True, 1, 0, 0, 0, 0.3333333333333333, 1, 1.0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0.09090909090909091, 0.0, 0.0, 0.0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            "JUGAR_MEDIA_MEJOR_OPCION":[0.3076923076923077, True, 0.46153846153846156, True, 0.6923076923076923, True, 1, 0, 0, 0, 0.3333333333333333, 1, 0.38461538461538464, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0.09090909090909091, 0.0, 0.0, 0.0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
            "MALDON":[0.0, True, 0.0, True, 0.0, True, 1, 0, 0, 0, 0.3333333333333333, 1, 0.38461538461538464, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0.12121212121212122, 0.0, 0.0, 0.0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            "BEST_HAND":[0.8461538461538461, True, 0.9230769230769231, True, 1.0, True, 1, 0, 0, 0, 0.3333333333333333, 1, 0.38461538461538464, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0.8484848484848485, 0.0, 0.0, 0.0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
            "HIGH_CARD_BEST_OPTION":[0.15384615384615385, True, 0.46153846153846156, False, 0.8461538461538461, True, 0, 1, 0, 0, 0.06666666666666667, 1, 0.6153846153846154, 1, 0.46153846153846156, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1.0, 0.0, 0.0, 0.25, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            "ME_CANTARON_ENVIDO": [0.15384615384615385, True, 0.23076923076923078, True, 0.3076923076923077, True, 1, 0, 0, 0, 0.3333333333333333, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1.0, 0.0, 0.0, 0.0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "ME_CANTARON_TRUCO": [0.15384615384615385, True, 0.23076923076923078, True, 0.3076923076923077, True, 1, 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1.0, 0.0, 0.0, 0.0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }


class QLearner(Player):
    
    def __init__(self, name, existingAlgoPath=None, n_hidden_1=240, learn='y'):
        super(QLearner, self).__init__()
        self.name = name
        self.dataFilePath = 'data.h5' # Where to save data for offline learning
        self.adapters = [CardUsage(), CurrentRound(), IAmHand(), CountPossibleActions(), RivalCardsUsed(), EnvidoAdapter(), MyEnvidoScore(), ScoreFeature(), TrucoLevel(), PossibleActionsBitMap(), HandsWon(), CompareCardsToOpponentsPlayedCard(), DesicionType()]
        self.m = self.getFeatureSetSize() # Sum of all adapter sizes
        self.X = np.empty((0,self.m), int) # INPUT of NN (state of game before action)
        self.ACTION = np.array([]) # ACTION taken for input X
        self.Y = np.array([]) # POINTS given for taking Action in game state (INPUT)
        # self.algorithm = QLearningNeuralNetwork(inputLayer=self.m, hiddenLayerSizes=(60,20), outputLayer=15, existingAlgoPath=existingAlgoPath)
        
        self.algorithm = QLearningTensorflow(n_input=self.m, n_hidden_1=n_hidden_1, outputLayer=15, existingAlgoPath=existingAlgoPath)
        # self.algorithm = QLearningRandomForest(newEstimatorsPerLearn=5)
        #self.algorithm = QLearningSGDRegressor()
        self.cardConverter = SimplifyValueCard()
        self.lr = 0.99 # LR for reward function
        self.C = 1000 # When to update target algorithm
        self.steps = 0 # Current steps from last update of target algorithm
        self.memorySize = 1000 # Size of memory for ExpRep
        self.trainSize = 32 # Expe Replay size
        self.epsilon = 1 # Probability of taking a random action
        self.epsilon_descent = 0.1 # Decrese every N learning steps
        self.epsilon_minimum = 0.1 # Minimum epslion
        self.epsilonIterations = 0
        if learn == 'n':
            self.doLearn = False
        else:
            self.doLearn = True
        # self.loadRandomTestDataset()
        self.countTargetUpdates = 0
        self.full_name = ('lr_' + str(self.lr) + '_' + 
                          'C_' + str(self.C) + '_' + 
                          'memorySize_' + str(self.memorySize) + '_' + 
                          'trainSize_' + str(self.trainSize) + '_' + 
                          'epsilon_descent_' + str(self.epsilon_descent) + '_' + 
                          'epsilon_minimum_' + str(self.epsilon_minimum) + '_' + 
                          'h1_' + str(n_hidden_1) + '_' + 
                          str(self.name))
        print(self.full_name,"QLearner created!")
    
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
        initialCardValues = [self.cardConverter.cardToFeature(c)[0] for c in initialCards]
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
        if(self.chooseRandomOption() and self.doLearn):
            return self.getRandomOption(requestDTO)

        yHatVector = self.algorithm.predict(np.array(self.getFeatureVector(requestDTO)).reshape(1,-1))
        action = self.getWinningPossibleAction(yHatVector, requestDTO)
        response = ActionTakenDTO()
        if(action in [ACTION.PLAYCARDLOW, ACTION.PLAYCARDMIDDLE, ACTION.PLAYCARDHIGH]):
            response.setCard(self.actionToCard(action, requestDTO.initialCards))
            action = ACTION.PLAYCARD
        response.setAction(action)
        return response
    
    def stopStartLearning(self):
        self.doLearn = not self.doLearn
        if self.doLearn:
            print("LEARNING")
        else:
            print("STOPED LEARNING")

    def audit(self):
        for situation, vector in AUDIT_DIC.iteritems():
            resultString = situation
            predictions = self.algorithm.predict(np.array(vector).reshape(1, -1), target=True)[0]
            for action in AUDIT_ACTIONS:
                action_index = ACTION.actionToIndexDic[action]
                resultString += " " + action + ":" + str(predictions[action_index])
            print(resultString)

    def printActionStats(self, possibleActions, preds):
        indexes = np.where(possibleActions)[0]
        for i in indexes:
            print(ACTION.actionToStringDic[i],preds[i])

    def learn(self, learnDTO):
        if self.doLearn:
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
            r = 1.0*learnDTO.points
            r /= 30.0 #Normalized
            # if r < 0:
            #     r*=2

            doPrint = np.random.rand(1) < 0.00001
            if doPrint:
                row = featureRows[0]
                possibleActions = possibleActionsRows[0]
                preds = self.algorithm.predict(np.array(row).reshape(1,-1), target=True)[0]
                self.printActionStats(possibleActions, preds)
            for Irow in range(1,len(featureRows)):
                # Rj + y * max(Q for all actions of next state [1:])
                # Target network hack
                row = featureRows[Irow]
                possibleActions = possibleActionsRows[Irow]
                if doPrint:
                    preds = self.algorithm.predict(np.array(row).reshape(1,-1), target=True)[0]
                    self.printActionStats(possibleActions, preds)
                yRows.append(0 + self.lr*max(self.algorithm.predict(np.array(row).reshape(1,-1), target=True)[0][possibleActions]))
            yRows.append(r) # Last action take got the points of the game

            # Experience Replay hack
            self.X = np.append(featureRows, self.X, axis = 0)
            self.ACTION = np.append(actionRows, self.ACTION, axis = 0)
            self.Y = np.append(yRows, self.Y, axis = 0)
            diff = self.Y.shape[0] - self.memorySize
            if self.Y.shape[0] > self.memorySize:
                self.X = self.X[:-diff]
                self.ACTION = self.ACTION[:-diff]
                self.Y = self.Y[:-diff]
            randomTrainIndexes = np.random.randint(0, min(self.memorySize, self.Y.shape[0]), min(self.Y.shape[0], self.trainSize))
            self.algorithm.learn(self.X[randomTrainIndexes,:], self.ACTION[randomTrainIndexes], self.Y[randomTrainIndexes])
            # self.saveDataset(np.array(featureRows), np.array(actionRows), np.array(yRows), np.array(possibleActionsRows)) # Save data for offline learning

            # Lower epsilon
            if self.epsilonIterations > 10000:
                newEpslion = self.epsilon*(1-self.epsilon_descent)
                print("EPSILON: ",newEpslion)
                if newEpslion > self.epsilon_minimum:
                    self.epsilon = newEpslion
                else:
                    self.epsilon = self.epsilon_minimum
                self.epsilonIterations = 0
            else:
                self.epsilonIterations += 1
            # Target network hack
            self.steps += 1
            if self.C < self.steps:
                self.countTargetUpdates += 1
                self.algorithm.updateTarget()
                self.audit()
                self.algorithm.updateLR()
                self.steps = 0
                #self.testConvergence()
                print("Target updated ", self.countTargetUpdates)
                if (self.countTargetUpdates < 500 and self.countTargetUpdates % 25 == 0) or (self.countTargetUpdates % 200 == 0):
                    self.save(os.path.join(os.getcwd(), self.full_name + '_' + str(self.countTargetUpdates)))

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

    def save(self, filePath):
        print("Saving to", filePath)
        self.algorithm.save(filePath)
        print("Save finished")


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
        actions = np.repeat(False,len(ACTION.actionToIndexDic))
        possibleActionsIndexs = self.getPossibleActionIndexes(requestDTO)
        for index in possibleActionsIndexs:
            actions[index] = True
        return actions

    #################################################################