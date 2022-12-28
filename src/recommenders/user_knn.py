from src.recommenders.recommender import Recommender
from lenskit.algorithms import user_knn
from pandas import DataFrame
from src.utils import process_parameters


class UserKNN(Recommender):
    def __init__(self, parameters: dict) -> None:
        """
        
        """

        default_keys = {
            'maxNumberNeighbors',
            'minNumberNeighbors',
            'min_sim',
            'feedback'
        }
        parameters = process_parameters(parameters, default_keys)

        self.max_number_neighbors = parameters['maxNumberNeighbors']
        self.min_number_neighbors = parameters['minNumberNeighbors']
        self.min_sim = parameters['min_sim']
        self.feedback = parameters['feedback']
        self.user_knn = user_knn.UserUser(
            nnbrs=self.max_number_neighbors,
            min_nbrs=self.min_number_neighbors,
            min_sim=self.min_sim,
            feedback=self.feedback
        )

    def predict_for_user(self, user, items, ratings=None):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        return self.user_knn.predict_for_user(
            user,
            items,
            ratings
        )

    def predict(self, user, items, ratings=None):
        """

        @param user:
        @param items:
        @return:
        """
        return self.user_knn.predict_for_user(
            user,
            items,
            ratings
        )

    def fit(self, ratings: DataFrame, **kwargs):
        """

        @param ratings:
        @param kwargs:
        @return:
        """
        self.user_knn.fit(ratings)
        return self.user_knn

    def recommend(self, user, n=None, candidates=None, ratings=None):
        pass

    def get_params(self, deep=True):
        pass
