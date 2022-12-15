from abc import ABC, abstractmethod

class Results(ABC):

    @abstractmethod
    def get_results(self):
        """
        
        """
        raise Exception("O método get_results de Results não está implementado")

class AbstractResults(Results):

    @abstractmethod
    def get_results(self):
        """
        
        """
        pass