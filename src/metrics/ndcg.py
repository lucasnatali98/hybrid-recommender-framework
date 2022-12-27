from src.metrics.metric import RankingMetric
import lenskit.metrics.topn as lenskit_topn
from sklearn.metrics import ndcg_score

class NDCG(RankingMetric):
    """


    """

    def __init__(self, parameters: dict) -> None:
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

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters:
        @return:
        """
        default_keys = set()
        parameters_keys_list = list(parameters.keys())

        parameters_keys = set()
        for parameter in parameters_keys_list:
            parameters_keys.add(parameter)

        if default_keys.issubset(parameters_keys):
            pass
        else:
            raise KeyError("Você não informou uma das chaves obrigatorias")


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

class NDCGScikit(RankingMetric):
    def __init__(self):
        """

        """
        pass

    def check_missing(self, truth, missing):
        """

        @param truth:
        @param missing:
        @return:
        """

        pass
    def evaluate(self, predictions, truth):
        """

        @param predictions: equivalente a y_true
        @param truth: equivalente a y_score?
        @return:
        """
        return ndcg_score(predictions, truth)

