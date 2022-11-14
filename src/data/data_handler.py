from dataclasses import dataclass
from src.data.folds import Folds
from abc import ABC, abstractmethod
@dataclass
class DataHandler:
    executable: str = None
    dataset: str = None
    factor: int = 0
    relevant: float = 0.0
    output_folder: str = ""

    def __init__(self):
        pass

    def run(self):
        """

        """
        pass

    def create_folds(self, strategy, data, n_splits, shuffle, random_state, **kwargs):
        folds = Folds(strategy)
        result_folds = folds.create_folds(data, n_splits, shuffle, random_state, kwargs)
        return result_folds

