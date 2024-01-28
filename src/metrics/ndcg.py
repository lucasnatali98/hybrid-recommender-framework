from src.metrics.metric import RankingMetric
import lenskit.metrics.topn as lenskit_topn
from sklearn.metrics import ndcg_score
from src.utils import process_parameters
import pandas as pd
import numpy as np


class NDCG(RankingMetric):
    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        raise NotImplementedError



class LenskitNDCG(NDCG):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        return lenskit_topn.ndcg(predictions, truth)


class SklearnNDCG(NDCG):
    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        predictions_array = predictions['score'].values.reshape(1, -1)
        truth_array = truth['rating'].values.reshape(1, -1)
        return ndcg_score(y_true=truth_array, y_score=predictions_array)