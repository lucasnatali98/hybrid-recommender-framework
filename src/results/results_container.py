from src.results.factory import *
from src.shared.container import Container

class ResultsContainer(Container):
    """

    """

    def __init__(self, parameters: dict) -> None:
        """
        @type stages: list

        """
        results = parameters['instances']

        if len(results) == 0:
            self.results_objects = []
        else:
            self.results_objects = []
            self.result_factory = ResultsFactory(parameters)
            self.results_objects = self.result_factory.create

