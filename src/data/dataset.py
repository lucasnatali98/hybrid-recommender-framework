from abc import ABC, abstractmethod
from src.data.loader import Loader


class Dataset(ABC):
    """
    Interface responsável por definir os métodos base das classes que representam
    uma base de dados comum em sistemas de recomendação
    """

    @property
    @abstractmethod
    def ratings(self):
        """

        """
        pass

    @property
    @abstractmethod
    def users(self):
        """
        
        """
        pass

    @property
    @abstractmethod
    def items(self):
        """
        
        """
        pass


class AbstractDataSet(Dataset):
    def __init__(self):
        self.Loader = Loader()

    @property
    @abstractmethod
    def ratings(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def users(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def items(self):
        raise NotImplementedError
