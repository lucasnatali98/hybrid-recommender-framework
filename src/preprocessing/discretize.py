from src.preprocessing.preprocessing import AbstractPreProcessing
from sklearn.preprocessing import KBinsDiscretizer


class DiscretizeProcessing(AbstractPreProcessing):

    def __init__(self):
        """
        
        """
        pass

    def pre_processing(self, data):
        encoder = KBinsDiscretizer(n_bins=5, encode="onehot")

        data = encoder.fit_transform(data)

        return data
