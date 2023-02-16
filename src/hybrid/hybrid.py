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
        self.constituent_algorithm = []
        self.metafeatures = []

    def add_metafeature(self, metafeature) -> None:
        """

        @param metafeature:
        @return:
        """
        self.metafeatures.append(metafeature)

    def remove_metafeature(self, metafeature):
        """

        @param metafeature:
        @return:
        """
        self.metafeatures.remove(metafeature)

    def add_algorithm(self, algorithm) -> None:
        """

        """
        self.constituent_algorithm.append(algorithm)

    def remove_algorithm(self, algorithm) -> None:
        """

        """
        self.remove_algorithm(algorithm)

    def _convert_metafeature_textfile_to_csv(self):
        pass
    def _read_metafeature_files(self, metafeatures):
        df = DataFrame()

    def combine_metafeature_with_predictions(self, metafeature: DataFrame, predictions: DataFrame) -> DataFrame:
        pass

    def set_weights(self, weights):
        pass



class HybridWeighted(Hybrid, ABC):

    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)


class HybridSwitching(Hybrid, ABC):

    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)


class HybridMixed(Hybrid, ABC):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)


hybrid = Hybrid({

})

loader = Loader()
