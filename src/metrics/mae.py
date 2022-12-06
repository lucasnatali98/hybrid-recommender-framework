from src.metrics.metric import PredictionMetric
import lenskit.metrics.predict as lenskit_predict


class MAE(PredictionMetric):
    """

    """
    def __init__(self, parameters: dict) -> None:
        """
        
        """
        pass

    def evaluate(self, predictions, truth):
        """

        @param predictions:
        @param truth:
        @return:
        """
        pass

    def check_missing(self, truth, missing):
        """

        """
        pass


class MAELensKit(PredictionMetric):
    """

    """
    def __init__(self):
        """

        """
        pass

    def evaluate(self, predictions, truth):
        """
        A função evaluate é responsável por aplicar a métrica MAE no resultados obtidos,
        esses resultados envolvem as predições feitas e também um ground truth para garantir
        a eficiencia da métrica

        @param: predictions
            -

        @param: truth
            -

        @return Lenskit - MAE

        """
        return lenskit_predict.mae(predictions, truth)

    def check_missing(self, truth, missing):
        """

        """
        pass