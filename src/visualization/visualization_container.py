from src.visualization.factory import *
from src.shared.container import Container

class VisualizationContainer(Container):
    """

    """

    def __init__(self, parameters: dict):
        """
        @type stages: list

        """
        visualizations = parameters['visualizations']

        if len(visualizations) == 0:
            self.visualizationObjects = []
        else:
            self.visualizationObjects = []
            self.visualization_factory = VisualizationFactory(parameters)
            self.visualizationObjects = self.visualization_factory.create


