from abc import ABC, abstractmethod


class Algorithm(ABC):

    @abstractmethod
    def fit(self, data, **kwargs) -> None:
        """
        Método para realizar o treinamento do algoritmo para os dados de classificação passados

        @param data: dados a serem treinados
        @param kwargs: argumentos adicionais
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

