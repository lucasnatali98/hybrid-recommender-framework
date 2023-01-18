from src.shared.container import Container
from src.shared.generic_factory import GenericFactory


class PreProcessingContainer(Container):
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


