from abc import ABC, abstractmethod

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
    def ratings(self):
        """
        
        """
        pass
    def users(self):
        """
        
        """
        pass
    def items(self):
        """
        
        """
        pass

