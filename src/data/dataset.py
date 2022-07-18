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

    def load(self, path, extension):
        pass


class AbstractDataSet(Dataset):
    """
        
    """

    def __init__(self):
        """

        """
        self.users = None
        self.movies = None
        self.ratings = None
        self.tags = None
        self.links = None
        self.genomeScores = None
        self.genomeTags = None
        self.Loader = Loader()

    def set_ratings(self, ratings):
        self.ratings = ratings

    def set_items(self, items):
        self.movies = items

    def set_users(self, users):
        self.users = users

    def set_tags(self, tags):
        self.tags = tags

    def ratings(self):
        """
        
        """
        return self.ratings

    def users(self):
        """
        
        """
        return self.users

    def items(self):
        """
        
        """
        pass
