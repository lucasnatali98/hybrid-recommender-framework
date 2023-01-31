from src.metrics.metric import PredictionMetric
import lenskit.metrics.predict as lenskit_predict
import pandas as pd
from src.utils import process_parameters

class MAE(PredictionMetric):
    """

    """
    def __init__(self, parameters: dict) -> None:
        """
        
        """
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        """

        @param predictions:
        @param truth:
        @return:
        """
        return lenskit_predict.mae(predictions, truth)


