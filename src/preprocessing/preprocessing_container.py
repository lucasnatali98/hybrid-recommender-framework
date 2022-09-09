from src.preprocessing.factories import *
from src.shared.container import Container
from src.shared.generic_factory import GenericFactory


class PreProcessingContainer(Container):
    """
    Preciso receber os parametros


    -> O tipo do parametro precisa ser padronizado

    -> toda classe precisa ter um método para interpretar

    https://stackoverflow.com/questions/482110
    4/dynamic-instantiation-from-string-name-of-a-class-in-dynamically-imported-module
    """

    def __init__(self, parameters: dict) -> None:
        """
        @type stages: list

        """

        super().__init__()
        stages = parameters['instances']

        if len(stages) == 0:
            pass
        else:
            self.processing_factory = GenericFactory(parameters)
            self.insert(0, self.processing_factory.create)


