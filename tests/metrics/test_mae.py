from src.metrics.mae import MAE
import pandas as pd
parameters = {
    "multioutput": "uniform_average"
}

mae = MAE(parameters)

class TestMAE:

    def test_evaluate(self):
        predictions = pd.Series()
        truth = pd.Series()
        mae.evaluate(predictions, truth)
