from src.preprocessing.preprocessing import AbstractPreProcessing
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, LabelEncoder
import pandas as pd
import numpy as np

ENCODING_TYPES = [
    "ordinal",
    "label",
    "onehot"
]


class EncodingProcessing(AbstractPreProcessing):

    def __init__(self, parameters: dict) -> None:
        """

        @rtype: object
        @param encoding_type:
        """
        super().__init__()
        encoding_type = parameters['encoding_type']

        encoding = list(filter(lambda x: x == encoding_type, ENCODING_TYPES))

        if len(encoding) == 0:
            raise Exception("Informe um método encoding válido")

        self.encoding_type = encoding[0]

    def _create_encoding_instance(self):
        """

        @return:
        """
        if self.encoding_type == "onehot":
            return OneHotEncoder()
        if self.encoding_type == "ordinal":
            return OrdinalEncoder()
        if self.encoding_type == "label":
            return LabelEncoder()

        return False

    def pre_processing(self, data, **kwargs):
        """

        @param data:
        @return:
        """
        encoding_instance = self._create_encoding_instance()
        data = np.array(data)
        data = data.reshape(1, -1)
        return encoding_instance.fit_transform(data)

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters: objeto com os parâmetros da classe
        @return: dicionário atualizado com esses mesmos parâmetros
        """

        pass

