from abc import ABC, abstractmethod
from src.data.loader import Loader


class Dataset(ABC):
    """
    
    
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

        """

        self.Loader = Loader()
        self.items = items
        self.ratings = ratings


    def ratings(self):
        """
        
        """
        return getattr(AbstractDataSet, 'ratings')

    def users(self):
        """
        
        """
        return self.users

    def items(self):
        """
        
        """
        return self.items
