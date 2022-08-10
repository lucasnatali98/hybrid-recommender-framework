from abc import ABC, abstractmethod


class Metric(ABC):

    @abstractmethod
    def evaluate(self, predictions, truth):
        """
        
        """
        pass

    @abstractmethod
    def check_missing(self, truth, missing):
        """
        
        """
        pass


class PredictionMetric(Metric):

    @abstractmethod
    def evaluate(self, predictions, truth):
        """
        
        """
        pass

    @abstractmethod
    def check_missing(self, truth, missing):
        """
        
        """
        pass


class RankingMetric(Metric):
    @abstractmethod
    def evaluate(self, predictions, truth):
        """
        
        """
        pass

    @abstractmethod
    def check_missing(self, truth, missing):
        """
        
        """
        pass
