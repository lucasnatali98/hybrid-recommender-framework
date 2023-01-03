import lenskit.metrics.topn as lenskit_topn
from src.metrics.metric import RankingMetric
from sklearn.metrics import recall_score
from src.utils import process_parameters, hrf_experiment_output_path
import pandas as pd


class Recall(RankingMetric):
    def __init__(self, parameters: dict) -> None:
        """

        """
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series):
        """

        @param predictions:
        @param truth:
        @return:
        """
        return lenskit_topn.recall(predictions, truth)

    def check_missing(self, truth: pd.Series, missing):
        """
        Check for missing truth values.
        Args:
            truth: the series of truth values
            missing: what to do with missing values

        """
        if missing == 'error' and truth.isna().any():
            missing = truth.isna().sum()
            raise ValueError('missing truth for {} predictions'.format(missing))
