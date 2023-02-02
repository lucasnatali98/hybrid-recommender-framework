from abc import ABC, abstractmethod
import pandas as pd


class Metric(ABC):

    @abstractmethod
    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
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


class AbstractMetric(Metric):
    @abstractmethod
    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        """

        @param predictions:
        @param truth:
        @return:
        """
        pass

    def check_missing(self, truth: pd.Series, missing):
        """
                        Check for missing truth values.
                        Args:
                            truth: the series of truth values
                            missing: what to do with missing values
                        """
        if missing == 'error' and truth.isna().any():
            missing = truth.isna().sum()
            raise ValueError('missing truth for {} predictions'.format(missing))


class PredictionMetric(AbstractMetric):

    @abstractmethod
    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        """

        @param predictions:
        @param truth:
        @return:
        """
        raise NotImplementedError


class RankingMetric(AbstractMetric):

    @abstractmethod
    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        """

        @param predictions:
        @param truth:
        @return:
        """
        raise NotImplementedError
