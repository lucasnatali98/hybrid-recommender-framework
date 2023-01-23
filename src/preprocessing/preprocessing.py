from abc import ABC, abstractmethod
import pandas as pd


class PreProcessing(ABC):
    @abstractmethod
    def pre_processing(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        
        """
        raise Exception("O método pre_processing não foi implementado")


class AbstractPreProcessing(PreProcessing):

    def __init__(self):
        pass

    @abstractmethod
    def pre_processing(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        pass
