from src.metrics.metric import PredictionMetric
import lenskit.metrics.predict as lenskit_predict
from src.utils import process_parameters
from sklearn.metrics import mean_squared_error
import pandas as pd


class RMSE(PredictionMetric):
    def __init__(self, parameters: dict) -> None:
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)
        self.parameters = parameters

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        raise NotImplementedError


class LenskitRMSE(RMSE):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        return lenskit_predict.rmse(predictions=predictions, truth=truth, missing='error')


class ScikitRMSE(RMSE):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        return mean_squared_error(truth, predictions, **kwargs)
