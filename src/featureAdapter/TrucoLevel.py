from __future__ import division

class TrucoLevel(object):
    """
        Return what level of truco are you in
    """
    size = 1
    def convert(self, requestDTO):
        level = requestDTO.getTrucoLevel()
        return [level/4]
