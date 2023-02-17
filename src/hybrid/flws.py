from src.hybrid.hybrid import HybridWeighted
from src.utils import process_parameters
from pandas import DataFrame, Series


class FLWS(HybridWeighted):
    def __init__(self, parameters: dict) -> None:
        """
        
        """
        super().__init__()
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)


    def run(self, metafeatures: DataFrame, predictions: DataFrame) -> DataFrame:
        """

        @return:
        """

