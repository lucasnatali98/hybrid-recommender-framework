from src.metrics.metric import PredictionMetric
import lenskit.metrics.predict as lenskit_predict


class MAE(PredictionMetric):
    """

    """
    def __init__(self):
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


class MAELensKit(PredictionMetric):
    """

    """
    def __init__(self):
        """

        """
        pass

    def evaluate(self, predictions, truth):
        """

        """
        return lenskit_predict.mae(predictions, truth)

    def check_missing(self, truth, missing):
        """

        """
        pass