from src.metrics.metric import DiversityMetric
from src.utils import process_parameters
import pandas as pd

import jpype
import jpype.imports
from jpype.types import *
from src.metrics.metric import DiversityMetric

class EILD(DiversityMetric):
    def __init__(self, parameters: dict) -> None:
        """

        """
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        raise NotImplementedError


class ImplementationEILD(EILD):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        return

