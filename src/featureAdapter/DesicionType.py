

"""
	Define if the decision (Quiero/NoQuiero)
	is related to Envido or Truco
	[On/Off, Related to Envido, Related to Truco]

"""
class DesicionType(object):
	size = 3

	def convert(self, requestDTO):
        desicionType = requestDTO.getDecisionType()
        if(desicionType == "Envido"):
        	return [1,1,0]
        elif(desicionType == "Truco"):
        	return [1,0,1]
        else:
        	return [0,0,0]
