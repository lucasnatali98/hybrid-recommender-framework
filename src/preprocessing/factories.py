from abc import abstractmethod

from src.preprocessing.preprocessing import PreProcessing
from src.preprocessing.encoding import EncodingProcessing
from src.preprocessing.split import SplitProcessing
from src.preprocessing.normalize import NormalizeProcessing
from src.preprocessing.discretize import DiscretizeProcessing


class Creator(PreProcessing):

    @abstractmethod
    def create(self) -> PreProcessing:
        pass


class EncodingProcessingFactory(Creator):

    def __init__(self):
        pass

    @property
    def create(self) -> PreProcessing:
        return EncodingProcessing()


class SplitProcessingFactory(Creator):

    def __init__(self):
        pass

    @property
    def create(self) -> PreProcessing:
        return SplitProcessing()


class DiscretizeProcessingFactory(Creator):
    def __init__(self):
        pass

    @property
    def create(self) -> PreProcessing:
        return DiscretizeProcessing()


class NormalizeProcessingFactory(Creator):

    def __init__(self):
        pass

    @property
    def create(self) -> PreProcessing:
        return NormalizeProcessing()
