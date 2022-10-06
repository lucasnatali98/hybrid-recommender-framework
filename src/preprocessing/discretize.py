from src.preprocessing.preprocessing import AbstractPreProcessing
from sklearn.preprocessing import KBinsDiscretizer


class DiscretizeProcessing(AbstractPreProcessing):

    def __init__(self, parameters: dict) -> None:
        """
        @rtype: object
        
        """
        pass

    def pre_processing(self, data, **kwargs):
        """

        @param **kwargs:
        @param data:
        @return:
        """
        encoder = KBinsDiscretizer(n_bins=5, encode="onehot")

        data = encoder.fit_transform(data)

        return data
