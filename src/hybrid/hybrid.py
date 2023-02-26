from pandas import DataFrame, Series
from src.data.loader import Loader
from abc import ABC, abstractmethod


class Hybrid(ABC):

    @abstractmethod
    def combine_metafeature_with_predictions(self, metafeature: DataFrame, predictions: DataFrame) -> DataFrame:
        """

        @param metafeature:
        @param predictions:
        @return:
        """
        pass

    @abstractmethod
    def set_weights(self, weights):
        pass

    @abstractmethod
    def predict(self, metafeatures, predictions):
        """

        @param metafeatures:
        @param predictions:
        @return:
        """
        pass


class AbstractHybrid(Hybrid):
    def __init__(self, parameters: dict) -> None:
        self.parameters = parameters
        self._constituent_algorithms= []
        self._metafeatures = []

    @property
    def metafeatures(self):
        return self._metafeatures

    @property
    def constituent_algorithms(self):
        return self._constituent_algorithms

    def add_metafeature(self, metafeature) -> None:
        """

        @param metafeature:
        @return:
        """
        self._metafeatures.append(metafeature)

    def remove_metafeature(self, metafeature):
        """

        @param metafeature:
        @return:
        """
        self._metafeatures.remove(metafeature)

    def add_algorithm(self, algorithm) -> None:
        """

        """
        self._constituent_algorithms.append(algorithm)

    def remove_algorithm(self, algorithm) -> None:
        """

        """
        self.remove_algorithm(algorithm)

    def combine_metafeature_with_predictions(self, metafeature: DataFrame, predictions: DataFrame) -> DataFrame:
        pass

    def set_weights(self, weights):
        pass


class HybridWeighted(AbstractHybrid, ABC):

    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)


class HybridSwitching(AbstractHybrid, ABC):

    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)



class HybridMixed(AbstractHybrid, ABC):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)

