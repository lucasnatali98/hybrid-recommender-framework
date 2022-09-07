from src.metrics.metric import Metric
from src.metrics.factory import *
from src.shared.container import Container

class MetricsContainer(Container):
    def __init__(self, parameters: dict):
        """

        """

        metrics = parameters['metrics']

        if len(metrics) == 0:
            self.metrics_objects = []
        else:
            self.metrics_objects = []
            self.metrics_factory = MetricsFactory(parameters)
            self.metrics_objects = self.metrics_factory.create


