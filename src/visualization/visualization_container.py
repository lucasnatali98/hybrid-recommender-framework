from src.shared.container import Container
from src.shared.generic_factory import GenericFactory

class VisualizationContainer(Container):
    """

    """

    def __init__(self, parameters: dict) -> None:
        """
        @type stages: list

        """
        super().__init__()
        visualizations = parameters['instances']

        if len(visualizations) == 0:
            pass
        else:
            self.visualization_factory = GenericFactory(parameters)
            self.insert(0, self.visualization_factory.create)


