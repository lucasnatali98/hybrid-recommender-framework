from src.metrics.metric import PredictionMetric
import lenskit.metrics.predict as lenskit_predict
import pandas as pd
from sklearn.metrics import mean_absolute_error
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
        raise NotImplementedError


class LenskitMAE(MAE):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        return lenskit_predict.mae(predictions, truth)


class ScikitMAE(MAE):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        return mean_absolute_error(truth, predictions, **kwargs)
