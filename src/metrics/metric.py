from abc import ABC, abstractmethod

class Metric(ABC):

    @abstractmethod
    def evaluate(self):
        """
        
        """
        pass

    @abstractmethod
    def check_missing(truth, missing):
        """
        
        """
        pass

class PredictionMetric(Metric):

    @abstractmethod
    def evalute(self):
        """
        
        """
        pass

    @abstractmethod
    def check_missing(truth, missing):
        """
        
        """
        pass


class RankingMetric(Metric):
    @abstractmethod
    def evalute(self):
        """
        
        """
        pass

    @abstractmethod
    def check_missing(truth, missing):
        """
        
        """
        pass