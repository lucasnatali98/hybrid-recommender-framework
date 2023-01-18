from src.preprocessing.preprocessing import AbstractPreProcessing
from sklearn.preprocessing import normalize
import numpy as np
from src.utils import process_parameters
import pandas as pd

class NormalizeProcessing(AbstractPreProcessing):

    def __init__(self, parameters: dict) -> None:
        """

        """
        super().__init__()
        default_keys = {
            'norm',
            'axis',
            'copy',
            'return_norm'
        }
        parameters = process_parameters(parameters, default_keys)
        self.norm = parameters.get('norm')
        self.axis = parameters.get('axis')
        self.copy = parameters.get('copy')
        self.return_norm = parameters.get('return_norm')

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

