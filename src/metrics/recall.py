import lenskit.metrics.topn as lenskit_topn
from src.metrics.metric import RankingMetric

class Recall(RankingMetric):
    def __init__(self, parameters: dict):
        """

        """
        pass

    def evaluate(self, predictions, truth):
        """

        @param predictions:
        @param truth:
        @return:
        """
        return lenskit_topn.recall(predictions, truth)

