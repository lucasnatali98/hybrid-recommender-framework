from src.preprocessing.preprocessing import AbstractPreProcessing
from sklearn.preprocessing import normalize


class NormalizeProcessing(AbstractPreProcessing):

    def __init__(self, parameters: dict) -> None:
        """

        """
        super().__init__()

    def pre_processing(self, data, **kwargs):
        """

        @param **kwargs:
        @param data:
        @return:
        """

        norm = kwargs.pop('norm')
        axis = kwargs.pop('axis')
        copy = kwargs.pop('copy')
        return_norm = kwargs.pop('return_norm')

        return normalize(
            X=data,
            norm=norm,
            axis=axis,
            copy=copy,
            return_norm=return_norm
        )
