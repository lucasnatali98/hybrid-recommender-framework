from src.preprocessing.preprocessing import AbstractPreProcessing
from sklearn.preprocessing import normalize
import numpy as np
import pandas as pd

class NormalizeProcessing(AbstractPreProcessing):

    def __init__(self, parameters: dict) -> None:
        """

        """
        super().__init__()
        self.process_parameters(parameters)
        self.norm = parameters['norm']
        self.axis = parameters['axis']
        self.copy = parameters['copy']
        self.return_norm = parameters['return_norm']


    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters: objeto com os parâmetros da classe
        @return: dicionário atualizado com esses mesmos parâmetros
        """

        default_keys = [
            'norm',
            'axis',
            'copy',
            'return_norm'
        ]
        parameters_keys = parameters.keys()

        for key in default_keys:
            if key not in parameters_keys:
                raise KeyError("A chave obrigatória {} não foi informada no arquivo de configuração".format(key))

        return parameters

    def pre_processing(self, data, **kwargs):
        """

        @param **kwargs:
        @param data:
        @return:
        """
        X = np.array(data['rating']).reshape(-1,1)

        normalized_data = normalize(
            X=X,
            norm=self.norm,
            axis=self.axis,
            copy=self.copy,
            return_norm=self.return_norm
        )
        normalized_data = normalized_data.flatten()

        data['rating'] = pd.Series(normalized_data)

        return data

