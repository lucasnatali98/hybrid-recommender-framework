from src.metrics.ndcg import NDCG
import pandas as pd
parameters = {
    "k": None,
    "sample_weight": None,
    "ignore_ties": False
}

ndcg = NDCG(parameters)

class TestNDCG:

    def test_evaluate(self):
        predictions = pd.Series()
        truth = pd.Series()
        ndcg.evaluate(predictions, truth)