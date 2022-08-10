import lenskit.metrics.topn as lenskit_topn
from src.metrics.metric import RankingMetric

class Recall(RankingMetric):
    def __init__(self):
        """

        """
        pass

    def evaluate(self, predictions, truth):
        """

        """
        return lenskit_topn.recall(predictions, truth)

