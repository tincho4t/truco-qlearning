from Player import Player
import sys
sys.path.insert(0, '../featureAdapter')
sys.path.insert(0, '../api')
from featureAdapter.SimplifyMyRemainingCards import SimplifyMyRemainingCards
from featureAdapter.MyEnvidoScore import MyEnvidoScore
from featureAdapter.RequestDTOFeature import RequestDTOFeature
from featureAdapter.CardUsage import CardUsage
from featureAdapter.HandsWon import HandsWon
from featureAdapter.CompareCardsToOpponentsPlayedCard import CompareCardsToOpponentsPlayedCard
import random
from api.dto.ActionTakenDTO import ActionTakenDTO
from api.dto.Action import Action


"""Test Player that choose an option randomly"""
class RulePlayer(Player):
    
    def __init__(self):
        super(RulePlayer, self).__init__()
        print "Rule player CREADO!!!!"
        self.adapters = [MyEnvidoScore(), HandsWon(), CompareCardsToOpponentsPlayedCard(), CardUsage()]

    def getAdapters(self):
        return self.adapters
    
    def learn(self, learnDTO):
        pass

    def getFeatureVector(self, requestDTO):
        featureVector = list()
        for adapter in self.getAdapters():
            featureVector += [adapter.convert(requestDTO)]
        return featureVector

    def play(self, requestDTO):
        x = self.getFeatureVector(requestDTO)
        response = self.chooseEnvido(requestDTO, x[0][0])
        if(response):
            return response
        else: # Hay que jugar el truco
            if self.haveToAccept(requestDTO): # Tengo que aceptar Truco
                return self.acceptTruco(requestDTO, x[3])
            else:
                return self.throwCard(requestDTO, x[3], x[2], x[1])

    def throwCard(self, requestDTO, cardUsage, cardsThatWin, handsWon):
        if(cardsThatWin[0]): # Tengo que matar la carta del oponente
            minCardToWin = self.getMinCardToWin(requestDTO.initialCards, cardsThatWin, cardUsage, handsWon)
            if(minCardToWin):
                return self.convertPlayCard(minCardToWin)
            else:
                return self.convertPlayCard(self.minCardNotPlayed(requestDTO.initialCards, cardUsage))
        else: # Tengo q jugar yo
            return self.convertPlayCard(self.greaterCardNotPlayed(requestDTO.initialCards, cardUsage)) # Siempre juego la mas alta

    """ Te indica si acepta o no el truco """
    def acceptTruco(self, requestDTO, cardUsage):
        # Si tengo al menos 2 cartas fuertes acepto
        # El nivel 7 para arriba son las cartas del 2 y mejores
        strongCardCount = (cardUsage[0]*13 >= 7) + (cardUsage[2]*13 >= 7) + (cardUsage[4]*13 >= 7)
        action = None
        if strongCardCount >= 1:
            action = "Quiero"
        else:
            action = "NoQuiero"
        return self.toResponse(action)

    """ Devuelve la minima carta que se puede ganar """
    def getMinCardToWin(self, initialCards, cardsThatWin, cardUsage, handsWon):
        # CardsThatWin = 1 hay carta del oponente + [gana mi carta i-esima, emparda mi carta i-esima, pierde mi carta i-esima] x 3
        # Mis cartas estan ordenadas de menor a mayor
        # Si empardo o gano con la mas baja la uso
        # Si perdi o emparde primera entonces solo pido ganar
        for i in range(3):
            if(cardUsage[i*2 + 1]): #If card is available
                thisIsSecondHand = handsWon[0]
                iWonSecondHand = handsWon[1]
                # If card beats current oponent or ties and I did good in first hand
                if(cardsThatWin[i*3 + 1] or (cardsThatWin[i*3 + 2] and (not thisIsSecondHand or iWonSecondHand))):
                    return initialCards[i]
        return None

    """ Devuelve la carta mas alta no jugada """
    def greaterCardNotPlayed(self, initialCards, cardUsage):
        # Iteramos de atras pa delante
        for i in range(3)[::-1]:
            if(cardUsage[i*2 + 1]):
                return initialCards[i]

    """ Devuelve la carta mas baja no jugada """
    def minCardNotPlayed(self, initialCards, cardUsage):
        for i in range(3):
            if(cardUsage[i*2 + 1]):
                return initialCards[i]

    # Tengo que aceptar o no el truco
    def haveToAccept(self, requestDTO):
        return "Quiero" in requestDTO.possibleActions

    def chooseEnvido(self, requestDTO, myEnvidoScore):
        score = myEnvidoScore * 33 # Desnormalizo el puntaje
        envido = requestDTO.getEnvido()
        envidoSung = envido.getSung()
        if not envido.isOpen():
            return None
        elif(len(envidoSung) > 0): # Me cantaron y tengo q decidir que hago
            lastSung = envidoSung[-1]
            if(lastSung == "FaltaEnvido"):
                return self.convertBoolean(score > 31)
            elif(len(envidoSung) == 1): # Me cantaron y tengo que definir que hacer
                return self.convertBoolean(score >= 27)
            else: # Cante y me subieron
                return self.convertBoolean(score > 28)
        elif score >= 32: # De aca en adelante Tengo que decidir si canto algo o no
            return self.toResponse("FaltaEnvido")
        elif score >= 26:
            return self.toResponse("Envido")
        else:
            return None

    def convertBoolean(self, boolean):
        action = "Quiero" if boolean else "NoQuiero"
        return self.toResponse(action)

    def convertPlayCard(self, card):
        response = ActionTakenDTO()
        response.setAction(Action.PLAYCARD)
        response.setCard(card)
        return response

    def toResponse(self, action):
        response = ActionTakenDTO()
        response.setAction(action)
        return response
