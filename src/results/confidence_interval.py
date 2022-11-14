from src.results.results import AbstractResults
from scipy.stats import t, norm


class ConfidenceInterval(AbstractResults):

    def __init__(self, parameters: dict) -> None:
        """
        
        """
        self.loc = parameters['loc']
        self.sigma = parameters['sigma']
        self.scale = parameters['scale']
        self.type = parameters['type']
        self.alpha = parameters['alpha']

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters: objeto com os parâmetros da classe
        @return: dicionário atualizado com esses mesmos parâmetros
        """

        pass

    def get_results(self):
        """

        @return:
        """
        if self.type == "norm":
            return norm.interval()

        if self.type == "t":
            return norm.interval()

        return None
