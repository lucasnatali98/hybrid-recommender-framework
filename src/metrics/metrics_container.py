from src.metrics.metric import Metric
from src.metrics.factories import *

class MetricsContainer:
    def __init__(self, parameters: dict):
        """

        """

        metrics = parameters['metrics']

        if len(metrics) == 0:
            self.metrics_objects = []
        else:
            self.metrics_objects = []
            self.metrics_factory = MetricsFactory(parameters)
            self.processingObjects = self.metrics_factory.create

    def push(self, metric: Metric):
        """

        @param metric:
        @return:
        """

        self.metrics.append(metric)

    def remove_all(self):
        """

        @return:
        """
        self.metrics.clear()

    def remove(self, metric: Metric):
        """

        @param metric:
        @return:
        """

        self.metrics.remove(metric)

    def insert(self, index: int, metric: Metric):
        """

        @param metric:
        @param index:

        @return:
        """
        self.metrics.insert(index, metric)

    def list(self):
        for metric in self.metrics:
            print(metric)
