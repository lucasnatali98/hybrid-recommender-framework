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
        result = ndcg.evaluate(predictions, truth)
        print(result)

    def test_check_missing(self):
        pass
