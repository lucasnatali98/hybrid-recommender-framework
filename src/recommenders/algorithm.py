from abc import ABC, abstractmethod


class Algorithm(ABC):

    @abstractmethod
    def fit(self, rating, **kwargs):
        """

        @param rating:
        @param kwargs:
        @return:
        """
        raise Exception("O método fit de Algorithm não está implementado")

    @abstractmethod
    def get_params(self, deep = True):
        """

        @param deep:
        @return:
        """
        pass

