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
        pass

    @abstractmethod
    def users(self):
        """
        
        """
        pass

    @abstractmethod
    def items(self):
        """
        
        """
        pass


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


