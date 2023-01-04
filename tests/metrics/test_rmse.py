from src.metrics.rmse import RMSE
import pandas as pd

parameters = {
    "sample_weight": "None",
    "squared": True,
    "missing": "error"

}

rmse = RMSE(parameters)


class TestRMSE:

    def test_evaluate(self):
        predictions = pd.Series([3, 4, 2, 1, 3, 5, 6])
        truth = pd.Series([2, 3, 2, 1, 5, 6, 1])
        result = rmse.evaluate(predictions, truth)

        print(result)

    def test_check_missing(self):
        pass