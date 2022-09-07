from src.preprocessing.factories import *
from src.shared.container import Container

class PreProcessingContainer(Container):
    """
    Preciso receber os parametros


    -> O tipo do parametro precisa ser padronizado

    -> toda classe precisa ter um método para interpretar

    https://stackoverflow.com/questions/482110
    4/dynamic-instantiation-from-string-name-of-a-class-in-dynamically-imported-module
    """

    def __init__(self, parameters: dict):
        """
        @type stages: list

        """

        super().__init__()
        stages = parameters['stages']

        if len(stages) == 0:
            self.processingObjects = []
        else:
            self.processingObjects = []
            self.processing_factory = ProcessingFactory(parameters)
            self.processingObjects = self.processing_factory.create

