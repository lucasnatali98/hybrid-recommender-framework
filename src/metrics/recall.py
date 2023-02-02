import lenskit.metrics.topn as lenskit_topn
from src.metrics.metric import RankingMetric
from sklearn.metrics import recall_score
from src.utils import process_parameters, hrf_experiment_output_path
import pandas as pd


class Recall(RankingMetric):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        raise NotImplementedError


class LenskitRecall(Recall):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        return lenskit_topn.recall(predictions, truth)


class ScikitRecall(Recall):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        return recall_score(truth, predictions)