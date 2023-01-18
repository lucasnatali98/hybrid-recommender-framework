from src.results.results import AbstractResults
from scipy.stats import t, norm
from src.utils import process_parameters


class ConfidenceInterval(AbstractResults):

    def __init__(self, parameters: dict) -> None:
        """
        
        """
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)
        self.loc = parameters.get('loc')
        self.sigma = parameters.get('sigma')
        self.scale = parameters.get('scale')
        self.type = parameters.get('type')
        self.alpha = parameters.get('alpha')

    def get_results(self):
        """

        @return:
        """
        if self.type == "norm":
            return norm.interval()

        if self.type == "t":
            return norm.interval()

        return None
