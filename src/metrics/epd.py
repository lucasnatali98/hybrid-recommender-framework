
from src.metrics.metric import RankingMetric


class EPD(RankingMetric):
    def __init__(self, parameters: dict) -> None:
        """
        
        """
        pass

    def evaluate(self):
        """

        """
        pass

    def process_parameters(self, parameters: dict) -> dict:
        """

        @return: dict
        """
        default_keys = set()
        parameters_keys_list = list(parameters.keys())

        parameters_keys = set()
        for parameter in parameters_keys_list:
            parameters_keys.add(parameter)

        if default_keys.issubset(parameters_keys):
            pass
        else:
            raise KeyError("Você não informou uma das chaves obrigatorias")
