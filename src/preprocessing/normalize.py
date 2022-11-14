from src.preprocessing.preprocessing import AbstractPreProcessing
from sklearn.preprocessing import normalize
import numpy as np

class NormalizeProcessing(AbstractPreProcessing):

    def __init__(self, parameters: dict) -> None:
        """

        """
        print("Normalize processing")
        self.norm = parameters['norm']
        self.axis = parameters['axis']
        self.copy = parameters['copy']
        self.return_norm = parameters['return_norm']
        super().__init__()

    def pre_processing(self, data, **kwargs):
        """

        @param **kwargs:
        @param data:
        @return:
        """


        X = np.array(data['rating']).reshape(-1,1)

        return normalize(
            X=X,
            norm=self.norm,
            axis=self.axis,
            copy=self.copy,
            return_norm=self.return_norm
        )


    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters: objeto com os parâmetros da classe
        @return: dicionário atualizado com esses mesmos parâmetros
        """

        pass
