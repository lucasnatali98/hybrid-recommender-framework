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

    def process_parameters(self, parameters: dict) -> dict:
        default_keys = set()
        parameters_keys_list = list(parameters.keys())

        parameters_keys = set()
        for parameter in parameters_keys_list:
            parameters_keys.add(parameter)

        if default_keys.issubset(parameters_keys):
            pass
        else:
            raise KeyError("Você não informou uma das chaves obrigatorias")


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

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters:
        @return:
        """
        pass