from src.recommenders.recommender import Recommender
from lenskit.algorithms import user_knn, Recommender
from pandas import DataFrame


class UserKNN(Recommender):
    def __init__(self, parameters: dict) -> None:
        """
        
        """
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

    def predict_for_users(self, user, items, ratings=None):
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

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters: objeto com os parâmetros da classe
        @return: dicionário atualizado com esses mesmos parâmetros
        """

        pass


