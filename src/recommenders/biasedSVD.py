from src.recommenders.recommender import Recommender
from src.utils import process_parameters

class BiasedSVD(Recommender):
    def __init__(self, parameters: dict) -> None:
        default_keys = {
            'iterations',
            'features'
        }

        parameters = process_parameters(parameters, default_keys)

        self.features = parameters['features']
        self.damping = parameters['damping']
#        self.bias = parameters['bias']
#       self.algorithm = parameters['algorithm']



    def predict_for_user(self, users, items, ratings):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        pass

    def predict(self, pairs, ratings):
        """

        @param pairs:
        @param ratings:
        @return:
        """
        pass

    def recommend(self, user, n, candidates, ratings):
        """

        @param user:
        @param n:
        @param candidates:
        @param ratings:
        @return:
        """
        pass

    def get_params(self, deep=True):
        """

        @param deep:
        @return:
        """
        pass

    def fit(self, rating, **kwargs):
        """

        @param rating:
        @param kwargs:
        @return:
        """
        pass