from abc import ABC

from src.metrics.metric import PredictionMetric
import lenskit.metrics.predict as lenskit_predict


class RMSE(PredictionMetric):
    """


    """
    def __init__(self):
        """
        
        """
        pass

    def evaluate(self):
        """
        
        """
        pass


class RMSELensKit(PredictionMetric):

    """


    """
    def __init__(self):
        pass

    def evaluate(self):
        pass

    def check_missing(self, truth, missing):
        lenskit_predict._check_missing(truth, missing)
