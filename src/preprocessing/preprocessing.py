from abc import ABC, abstractmethod


class PreProcessing(ABC):

    @abstractmethod
    def pre_processing(self, data, **kwargs):
        """
        
        """
        raise Exception("O método pre_processing não foi implementado")



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



