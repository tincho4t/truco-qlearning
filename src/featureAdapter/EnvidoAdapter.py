from __future__ import division

class EnvidoAdapter(object):
    size = 1 + 2 + 20 # EnvidoOpen, Opponent Points, EnvidoSung
    MAX_ENVIDO_SCORE = 33
    def convert(self, requestDTO):
    	return self.getFeatures(requestDTO.getEnvido())

    def getFeatures(self, envidoDTO):
        feature = list()
        feature.append( 1 if envidoDTO.isOpen() else 0)
        opponentEnvido = envidoDTO.getOppenentEnvidoScore()
        if(opponentEnvido != None and opponentEnvido != -1):
        	feature.append(1) # Envido opponent is Set
        	feature.append(opponentEnvido / self.MAX_ENVIDO_SCORE)
        else:
        	feature.append(0) # Envido opponent wasn't Set
        	feature.append(0)
        feature += self.getSungFeature(envidoDTO)
        return feature

    def getSungFeature(self, envidoDTO):
    	envF = []
    	i = 5;
        for sung in envidoDTO.getSung():
        	envidoConverted = [0,0,0,0]
        	envidoConverted[self.envidoToIndex(sung)] = 1 # Set the bit
        	envF += envidoConverted
        	i -= 1
        for j in range(0,i):
        	envF += [1,0,0,0]
        return envF

    def envidoToIndex(self, envido):
    	return {
            "Nothing": 0,
    		"Envido": 1,
    		"RealEnvido": 2,
    		"FaltaEnvido": 3
    	}[envido]
