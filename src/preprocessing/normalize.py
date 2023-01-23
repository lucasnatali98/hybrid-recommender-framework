from src.preprocessing.preprocessing import AbstractPreProcessing
from sklearn.preprocessing import normalize
import numpy as np
from src.utils import process_parameters
import pandas as pd

class NormalizeProcessing(AbstractPreProcessing):
    def __init__(self, parameters: dict) -> None:

        super().__init__()
        default_keys = {
            'norm',
            'axis',
            'copy',
            'return_norm'
        }
        parameters = process_parameters(parameters, default_keys)
        self.column_to_apply = parameters.get("column_to_apply", 'rating')
        self.norm = parameters.get('norm')
        self.axis = parameters.get('axis')
        self.copy = parameters.get('copy')
        self.return_norm = parameters.get('return_norm')

    def pre_processing(self, data: pd.DataFrame, **kwargs):
        """
        Função de preprocessamento para realizar a normalização em uma coluna especifica
        do dataframe informado (data)

        @param data: pd.DataFrame
        @param **kwargs: parâmetros adicionais da função de preprocessamento
        @return: um novo dataframe com uma coluna que contém o resultado da normalizaçãp
        """

        X = np.array(data[self.column_to_apply]).reshape(-1,1)

        normalized_data = normalize(
            X=X,
            norm=self.norm,
            axis=self.axis,
            copy=self.copy,
            return_norm=self.return_norm
        )
        normalized_data = normalized_data.flatten()
        data[self.column_to_apply] = pd.Series(normalized_data)
        return data

