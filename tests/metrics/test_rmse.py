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
        predictions = pd.Series()
        truth = pd.Series()
        result = rmse.evaluate(predictions, truth)
        print(result)
