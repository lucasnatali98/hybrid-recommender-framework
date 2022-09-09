from src.results.factory import *
from src.shared.container import Container
from src.shared.generic_factory import GenericFactory

class ResultsContainer(Container):
    """

    """

    def __init__(self, parameters: dict) -> None:
        """
        @type stages: list

        """
        super().__init__()
        results = parameters['instances']

        if len(results) == 0:
            pass
        else:
            self.result_factory = GenericFactory(parameters)
            self.insert(0, self.result_factory.create)

