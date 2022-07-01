from abc import ABC, abstractmethod


class Algorithm(ABC):

    @abstractmethod
    def fit(self, rating, **kwargs):
        """
        
        """
        pass

    @abstractmethod
    def get_params(self, deep = True):
        """
        
        """
        pass