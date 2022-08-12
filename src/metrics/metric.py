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


class PredictionMetric(Metric):

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


class RankingMetric(Metric):
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
