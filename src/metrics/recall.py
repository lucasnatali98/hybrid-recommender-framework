import lenskit.metrics.topn as lenskit_topn
from src.metrics.metric import RankingMetric
from sklearn.metrics import recall_score
class Recall(RankingMetric):
    def __init__(self, parameters: dict) -> None:
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

    def check_missing(self, truth, missing):
        """

        @param truth:
        @param missing:
        @return:
        """
        pass

class RecallScikit(RankingMetric):
    def __init__(self) -> None:
        """

        """
        pass

    def evaluate(self, predictions, truth):
        """

        @param predictions:
        @param truth:
        @return:
        """
        return recall_score(predictions, truth)


    def check_missing(self, truth, missing):
        """

        @param truth:
        @param missing:
        @return:
        """
        pass