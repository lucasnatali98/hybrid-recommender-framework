from abc import abstractmethod

from src.recommenders.recommender import Recommender
from lenskit.algorithms import user_knn, Recommender as LenskitRecommender
from pandas import DataFrame
from src.utils import process_parameters
import pandas as pd


class UserKNN(Recommender):
    def __init__(self, parameters: dict) -> None:
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def recommend(self, users, n, candidates=None, ratings=None) -> pd.DataFrame:
        raise NotImplementedError

    def predict(self, pairs, ratings):
        raise NotImplementedError

    def predict_for_user(self, user, items, ratings):
        raise NotImplementedError

    def fit(self, rating, **kwargs) -> None:
        raise NotImplementedError

    def get_params(self, deep=True):
        raise NotImplementedError


class LenskitUserKNN(UserKNN):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = {
            'maxNumberNeighbors'
        }
        parameters = process_parameters(parameters, default_keys)

        self.max_number_neighbors = parameters.get('maxNumberNeighbors')
        self.min_number_neighbors = parameters.get('minNumberNeighbors')
        self.min_sim = parameters.get('min_sim')
        self.feedback = parameters.get('feedback')

        self.user_knn = user_knn.UserUser(
            nnbrs=self.max_number_neighbors,
            # min_nbrs=self.min_number_neighbors, #parâmetro dando problema
            # min_sim=self.min_sim,
            # feedback=self.feedback
        )
        self.user_knn = LenskitRecommender.adapt(self.user_knn)

    @property
    def recommender(self):
        return self.user_knn

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

    def predict(self, pairs, ratings):
        return self.user_knn.predict(
            pairs,
            ratings)

    def fit(self, ratings: DataFrame, **kwargs) -> None:
        return self.user_knn.fit(ratings)

    def recommend(self, users, n=None, candidates=None, n_jobs=None) -> pd.DataFrame:
        recommendation_dataframe = pd.DataFrame(
            columns=['user', 'item', 'score', 'algorithm_name']
        )
        for user in users:
            recommendation_to_user = self.user_knn.recommend(user, n)

            names = pd.Series([self.__class__.__name__] * n)
            user_id_list = pd.Series([user] * n)

            recommendation_to_user['algorithm_name'] = names
            recommendation_to_user['user'] = user_id_list

            recommendation_dataframe = pd.concat(
                [recommendation_dataframe, recommendation_to_user],
                ignore_index=True
            )

        return recommendation_dataframe

    def get_params(self, deep=True):
        pass
