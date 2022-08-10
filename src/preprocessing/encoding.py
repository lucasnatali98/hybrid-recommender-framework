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

    def __init__(self, encoding_type):
        """
        
        """
        super().__init__()

        encoding = filter(lambda x: x == encoding_type, ENCODING_TYPES)
        encoding = list(encoding)

        if len(encoding) == 0:
            raise Exception("Informe um método encoding válido")

        self.encoding_type = encoding[0]

    def _create_encoding_instance(self):
        if self.encoding_type == "onehot":
            return OneHotEncoder()
        if self.encoding_type == "ordinal":
            return OrdinalEncoder()
        if self.encoding_type == "label":
            return LabelEncoder()

        return False

    def pre_processing(self, data):
        encoding_instance = self._create_encoding_instance()
        data = np.array(data)
        data = data.reshape(1, -1)
        print(data)
        return encoding_instance.fit_transform(data)
