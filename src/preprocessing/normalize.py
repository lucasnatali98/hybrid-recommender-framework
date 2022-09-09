from src.preprocessing.preprocessing import AbstractPreProcessing
from sklearn.preprocessing import normalize


class NormalizeProcessing(AbstractPreProcessing):

    def __init__(self, parameters: dict)-> None:
        """

        """
        super().__init__()

    def pre_processing(self, data):
        """

        @param data:
        @return:
        """
        return normalize(data)
