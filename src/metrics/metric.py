from abc import ABC, abstractmethod
import pandas as pd

class Metric(ABC):

    @abstractmethod
    def evaluate(self, predictions: pd.Series, truth: pd.Series):
        """

        @param predictions:
        @param truth:
        @return:
        """
        raise Exception("O método evaluate de Metric não está implementado")

    @abstractmethod
    def check_missing(self, truth: pd.Series, missing):
        """

        @param truth:
        @param missing:
        @return:
        """
        raise Exception("O método check_missing de Metric não está implementado")


class AbstractMetric(Metric):
    @abstractmethod
    def evaluate(self, predictions: pd.Series, truth: pd.Series):
        """

        @param predictions:
        @param truth:
        @return:
        """
        pass

    @abstractmethod
    def check_missing(self, truth: pd.Series, missing):
        """

        @param truth:
        @param missing:
        @return:
        """
        pass

class PredictionMetric(AbstractMetric):

    @abstractmethod
    def evaluate(self, predictions: pd.Series, truth: pd.Series):
        """

        @param predictions:
        @param truth:
        @return:
        """
        pass

    @abstractmethod
    def check_missing(self, truth: pd.Series, missing):
        """

        @param truth:
        @param missing:
        @return:
        """
        pass


class RankingMetric(AbstractMetric):
    @abstractmethod
    def evaluate(self, predictions: pd.Series, truth: pd.Series):
        """

        @param predictions:
        @param truth:
        @return:
        """
        pass

    @abstractmethod
    def check_missing(self, truth: pd.Series, missing):
        """

        @param truth:
        @param missing:
        @return:
        """
        pass
