from abc import ABC, abstractmethod
from src.data.loader import Loader


class Dataset(ABC):
    """
    Interface responsável por definir os métodos base das classes que representam
    uma base de dados comum em sistemas de recomendação
    
    """

    @abstractmethod
    def ratings(self):
        """
        
        """
        raise Exception("O método ratings de Dataset não está implementado")

    @abstractmethod
    def users(self):
        """
        
        """
        raise Exception("O método users de Dataset não está implementado")

    @abstractmethod
    def items(self):
        """
        
        """
        raise Exception("O método items de Dataset não está implementado")

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters:
        @return:
        """
        raise Exception("O método process_parameters de Dataset não foi implementado")


class AbstractDataSet(Dataset):
    """
        
    """

    def __init__(self, items=None, ratings=None, links=None, tags=None):
        """

        @param items:
        @param ratings:
        @param links:
        @param tags:
        """

        self.Loader = Loader()





    def ratings(self):
        """

        @return:
        """
        return self.ratings


    def users(self):
        """

        @return:
        """
        return self.users


    def items(self):
        """

        @return:
        """
        return self.items


