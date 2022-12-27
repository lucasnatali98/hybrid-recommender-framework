from lenskit.batch import recommend, predict
class Batch:
    def __init__(self):
        pass

    def recommend(self, algorithms: list = None, users = None, n = None, candidates = None, n_jobs = None):
        pass

    def predict(self, algorithms: list = None, pairs = None, n_jobs: int = None):
        pass