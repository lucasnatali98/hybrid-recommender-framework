from abc import ABC, abstractmethod
import sklearn


class PreProcessing(ABC):

    @abstractmethod
    def pre_processing():
        """
        
        """
        pass

def AbstractPreProcessing(PreProcessing):

    def __init__(self):
        """
        
        """
        pass
    @abstractmethod
    def pre_processing():
        """
        
        """
        pass

def PreProcessingContainer():
    def __init__(self):
        self.processingObjects = []

    def push_back(self, obj):
        """
        
        """
        pass

    def push_front(self, obj):
        """
        
        """
        pass

    def remove(self, obj):
        """
        
        """
        pass

    def removeAll(self):
        """
        
        """
        pass