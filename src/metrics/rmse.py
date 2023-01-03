from src.metrics.metric import PredictionMetric
import lenskit.metrics.predict as lenskit_predict
from src.utils import process_parameters
import pandas as pd

class RMSE(PredictionMetric):
    def __init__(self, parameters: dict) -> None:
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)
        self.parameters = parameters


    def evaluate(self, predictions: pd.Series, truth: pd.Series):
        """

        @param predictions:
        @param truth:
        @return:
        """
        return lenskit_predict.rmse(predictions=predictions, truth=truth, missing='error')

    def check_missing(self, truth, missing):
        """
                  Check for missing truth values.
                  Args:
                      truth: the series of truth values
                      missing: what to do with missing values
                  """
        if missing == 'error' and truth.isna().any():
            missing = truth.isna().sum()
            raise ValueError('missing truth for {} predictions'.format(missing))


