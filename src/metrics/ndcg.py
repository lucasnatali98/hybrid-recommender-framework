from src.metrics.metric import RankingMetric
import lenskit.metrics.topn as lenskit_topn


class NDCG(RankingMetric):
    """


    """

    def __init__(self, parameters: dict):
        """
        
        """
        pass

    def evaluate(self, predictions, truth):
        """
        
        """
        pass

    def check_missing(self, truth, missing):
        """

        """
        pass


class NDCGLenskit(RankingMetric):
    """

    """

    def __init__(self):
        """

        """
        pass

    def evaluate(self, predictions, truth):
        """

        @param predictions:
        @param truth:
        @return:
        """
        return lenskit_topn.ndcg(predictions, truth)

    def check_missing(self, truth, missing):
        """

        """
        pass
