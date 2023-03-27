from pandas import DataFrame, Series
from src.data.loader import Loader
from abc import ABC, abstractmethod
from src.recommenders.recommender import Recommender

"""
Na hibridização eu vou precisar especializar os métodos dentro de cada classe
isso porque cada abordagem tem suas necessidades e caracteristicas, por exemplo,
a definição de pesos faz sentido caso estejamos considerando 

"""


class Hybrid(Recommender):  # herdar de recommender novamente
    @abstractmethod
    def add_constituent(self, constituent):
        pass

    @abstractmethod
    def update_constituent(self, const_id, new_constituent):
        pass

    @abstractmethod
    def remove_constituent(self, const_id):
        pass


class AbstractHybrid(Hybrid):
    def __init__(self, parameters: dict) -> None:
        self.parameters = parameters
        self._constituent_algorithms = []


    def fit(self, data, **kwargs) -> None:
        raise NotImplementedError
    def recommend(self, users, n, candidates=None, ratings=None) -> DataFrame:
        raise NotImplementedError
    def predict_for_user(self, user, items, ratings):
        raise NotImplementedError
    def get_params(self, deep = True):
        raise NotImplementedError
    @property
    def metafeatures(self):
        return self._metafeatures

    @property
    def constituent_algorithms(self):
        return self._constituent_algorithms

    def add_constituent(self, algorithm) -> None:
        """

        """
        self._constituent_algorithms.append(algorithm)

    def update_constituent(self, const_id, new_constituent):
        """

        """
        pass
    def remove_constituent(self, algorithm) -> None:
        """

        """
        self._constituent_algorithms.remove(algorithm)

    def combine_metafeature_with_predictions(self, metafeature: DataFrame, predictions: DataFrame) -> DataFrame:
        pass


class HybridWeighted(AbstractHybrid, ABC):

    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        self._metafeatures = []
        #self.features =[]

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

    # Eu insiro as metafeatures
    @abstractmethod
    def set_weights(self, weights):
        pass



    @abstractmethod
    def combine_metafeature_with_predictions(self, metafeature: DataFrame, predictions: DataFrame) -> DataFrame:
        """

        @param metafeature:
        @param predictions:
        @return:
        """
        pass


class HybridSwitching(AbstractHybrid, ABC):

    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)


class HybridMixed(AbstractHybrid, ABC):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
