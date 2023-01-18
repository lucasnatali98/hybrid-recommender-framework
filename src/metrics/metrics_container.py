from src.metrics.metric import Metric
from src.shared.container import Container
from src.shared.generic_factory import GenericFactory


class MetricsContainer(Container):
    """

    """

    def __init__(self, parameters: dict) -> None:
        """

        """
        super().__init__()
        metrics = parameters.get('instances')

        if len(metrics) == 0:
            pass
        else:
            self.metrics_factory = GenericFactory(parameters)
            self.insert(0, self.metrics_factory.create)
