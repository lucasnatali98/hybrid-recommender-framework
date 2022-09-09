from src.metrics.metric import Metric
from src.metrics.factory import *
from src.shared.container import Container

class MetricsContainer(Container):
    """

    """
    def __init__(self, parameters: dict) -> None:
        """

        """
        super().__init__()
        metrics = parameters['instances']

        if len(metrics) == 0:
            pass
        else:
            self.metrics_factory = MetricsFactory(parameters)
            self.insert(0, self.metrics_factory.create)


