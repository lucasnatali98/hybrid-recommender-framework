from src.metrics.metric import RankingMetric
import lenskit.metrics.topn as lenskit_topn
from src.utils import process_parameters
import pandas as pd


class DCG(RankingMetric):
    def __init__(self, parameters: dict) -> None:
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        raise NotImplementedError



class LenskitDCG(DCG):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        return lenskit_topn.dcg(predictions, truth)
