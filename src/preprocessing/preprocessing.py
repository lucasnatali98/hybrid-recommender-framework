from abc import ABC, abstractmethod


class PreProcessing(ABC):

    @abstractmethod
    def pre_processing(self, data, **kwargs):
        """
        
        """
        raise Exception("O método pre_processing não foi implementado")

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters:
        @return:
        """
        raise Exception("O método process_parameters não foi implementado")



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



