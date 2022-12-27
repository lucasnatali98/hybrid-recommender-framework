from src.results.results import AbstractResults
from scipy.stats import t, norm
from src.utils import process_parameters


class ConfidenceInterval(AbstractResults):

    def __init__(self, parameters: dict) -> None:
        """
        
        """
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)
        self.loc = parameters['loc']
        self.sigma = parameters['sigma']
        self.scale = parameters['scale']
        self.type = parameters['type']
        self.alpha = parameters['alpha']

    def get_results(self):
        """

        @return:
        """
        if self.type == "norm":
            return norm.interval()

        if self.type == "t":
            return norm.interval()

        return None
