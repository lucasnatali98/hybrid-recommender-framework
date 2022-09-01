from abc import ABC, abstractmethod


class Metric(ABC):

    @abstractmethod
    def evaluate(self, predictions, truth):
        """

        @param predictions:
        @param truth:
        @return:
        """
        pass

    @abstractmethod
    def check_missing(self, truth, missing):
        """

        @param truth:
        @param missing:
        @return:
        """
        pass


class AbstractMetric(Metric):
    @abstractmethod
    def evaluate(self, predictions, truth):
        """

        @param predictions:
        @param truth:
        @return:
        """
        pass

    @abstractmethod
    def check_missing(self, truth, missing):
        """

        @param truth:
        @param missing:
        @return:
        """
        pass

class PredictionMetric(AbstractMetric):

    @abstractmethod
    def evaluate(self, predictions, truth):
        """

        @param predictions:
        @param truth:
        @return:
        """
        pass

    @abstractmethod
    def check_missing(self, truth, missing):
        """

        @param truth:
        @param missing:
        @return:
        """
        pass


class RankingMetric(AbstractMetric):
    @abstractmethod
    def evaluate(self, predictions, truth):
        """

        @param predictions:
        @param truth:
        @return:
        """
        pass

    @abstractmethod
    def check_missing(self, truth, missing):
        """

        @param truth:
        @param missing:
        @return:
        """
        pass
