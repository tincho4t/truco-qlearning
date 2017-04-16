from __future__ import division

class ScoreFeature(object):
    """
        Return your score and opponent score
    """
    size = 2
    def convert(self, requestDTO):
        score = requestDTO.getScore()
        return [score.myScore / score.scoreToWin, score.opponentScore / score.scoreToWin]
