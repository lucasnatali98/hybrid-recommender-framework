from abc import ABC, abstractmethod
import sklearn



class PreProcessing(ABC):

    @abstractmethod
    def pre_processing(self, data):
        """
        
        """
        pass


class AbstractPreProcessing(PreProcessing):

    def __init__(self):
        """
        
        """
        pass

    @abstractmethod
    def pre_processing(self, data):
        """
        
        """
        pass


