from src.preprocessing.preprocessing import AbstractPreProcessing
from sklearn.preprocessing import normalize


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

        print("kwargs")
        print(**kwargs)


        return normalize(
            X=data,
            norm=self.norm,
            axis=self.axis,
            copy=self.copy,
            return_norm=self.return_norm
        )
