from Player import Player
import sys
sys.path.insert(0, '../featureAdapter')
sys.path.insert(0, '../api')
from featureAdapter.SimplifyMyRemainingCards import SimplifyMyRemainingCards
from featureAdapter.MyEnvidoScore import MyEnvidoScore
from featureAdapter.RequestDTOFeature import RequestDTOFeature
import random
from api.dto.ActionTakenDTO import ActionTakenDTO
from api.dto.Action import Action


"""Test Player that choose an option randomly"""
class RulePlayer(Player):
    
    def __init__(self):
        super(Randomio, self).__init__()
        print "Rule player CREADO!!!!"
        self.adapters = [RequestDTOFeature(), MyEnvidoScore(), HandsWon(), CompareCardsToOpponentsPlayedCard()]

    def getAdapters(self):
        return self.adapters
    
    def learn(self, learnDTO):
        print "Lerning... ", learnDTO
    
    def predict(self, x):
        requestDTO = x[0]
        response = self.chooseEnvido(requestDTO, x[1])
        if(response):
            return response
        else: # Hay que jugar el truco
            if self.haveToAccept(requestDTO): # Tengo que aceptar Truco
                return self.acceptTruco(requestDTO, x[2])
            else:
                return self.play(requestDTO, x[3])

    def play(self, requestDTO, cardsThatWin):
        if(cardsThatWin[0]): # Tengo que matar la carta del oponente
            minCardToWin = self.getMinCardToWin()
            if(minCardToWin):
                return self.convertPlayCard(minCardToWin)
            else:
                return self.convertPlayCard(self.minCardNotPlayed())
        else: # Tengo q jugar yo
            return self.greaterCardNotPlayer() # Siempre juego la mas alta

    """ Te indica si acepta o no el truco """
    def acceptTruco(self, requestDTO, handsWon):
        return "Quiero" #TODO: Poner logica aca que tenga sentido

    """ Devuelve la minima carta que se puede ganar """
    def getMinCardToWin(self):
        pass #TODO:

    """ Devuelve la carta mas alta no jugada """
    def greaterCardNotPlayer(self):
        pass #TODO dev

    """ Devuelve la carta mas baja no jugada """
    def minCardNotPlayed(self):
        pass #TODO

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
