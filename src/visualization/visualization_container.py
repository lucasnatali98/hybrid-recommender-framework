from src.visualization.factory import *
from src.shared.container import Container

class VisualizationContainer(Container):
    """

    """

    def __init__(self, parameters: dict) -> None:
        """
        @type stages: list

        """
        super().__init__(self)
        visualizations = parameters['instances']

        if len(visualizations) == 0:
            self.visualizationObjects = []
        else:
            self.visualizationObjects = []
            self.visualization_factory = VisualizationFactory(parameters)
            self.visualizationObjects = self.visualization_factory.create


