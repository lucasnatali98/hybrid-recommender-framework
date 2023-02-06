from abc import ABC, abstractmethod
from src.utils import process_parameters

from lenskit.batch import recommend, predict


class Batch(ABC):
    @abstractmethod
    def recommend(self, algorithm, users=None, n=None, candidates=None, n_jobs=None):
        pass

    @abstractmethod
    def predict(self, algorithms=None, pairs=None, n_jobs: int = None):
        pass


class LenskitBatch(Batch):
    def __init__(self, parameters: dict = {}) -> None:
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def recommend(self, algorithm, users=None, n=None, candidates=None, n_jobs=None):
        return recommend(
            algo=algorithm,
            users=users,
            n=n,
            candidates=candidates,
            n_jobs=n_jobs
        )

    def predict(self, algorithm=None, pairs=None, n_jobs: int = None):
        return predict(algorithm, pairs)

