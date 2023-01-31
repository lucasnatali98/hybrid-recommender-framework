from src.metrics.metric import RankingMetric
import lenskit.metrics.topn as lenskit_topn
from sklearn.metrics import ndcg_score
from src.utils import process_parameters
import pandas as pd


class NDCG(RankingMetric):
    def __init__(self, parameters: dict) -> None:
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        """
        
        """
        return lenskit_topn.ndcg(predictions, truth)

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
