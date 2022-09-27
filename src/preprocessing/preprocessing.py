from abc import ABC, abstractmethod


class PreProcessing(ABC):

    @abstractmethod
    def pre_processing(self, data, **kwargs):
        """
        
        """
        pass


class AbstractPreProcessing(PreProcessing):

    def __init__(self):
        """
        
        """
        pass

    @abstractmethod
    def pre_processing(self, data, **kwargs):
        """
        
        """
        pass


