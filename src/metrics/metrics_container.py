from src.metrics.metric import Metric



class MetricsContainer:
    def __init__(self):
        """

        """
        self.metrics = []

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