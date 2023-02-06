import pandas as pd
from lenskit.algorithms.basic import Random
from src.recommenders.recommender import Recommender
from src.utils import process_parameters
from lenskit.algorithms import Recommender as LenskitRecommender
from pandas import DataFrame, Series, concat



class RandomItem(Recommender):
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


class LenskitRandomItem(RandomItem):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)
        self.parameters = parameters
        self.RandomItem = Random()


    def fit(self, ratings: DataFrame, **kwargs):
        self.RandomItem.fit(ratings)

    def recommend(self, users, n, candidates = None, ratings = None):
        recommendation_dataframe = DataFrame(
            columns=['user', 'item', 'score', 'algorithm_name']
        )
        for user in users:
            recommendation_to_user = self.RandomItem.recommend(user, n, candidates, ratings)

            names = Series([self.__class__.__name__] * n)
            user_id_list = Series([user] * n)

            recommendation_to_user['algorithm_name'] = names
            recommendation_to_user['user'] = user_id_list

            recommendation_dataframe = concat(
                [recommendation_dataframe, recommendation_to_user],
                ignore_index=True
            )

        return recommendation_dataframe

    def predict_for_user(self, user, items, ratings=None):
        return None

    def predict(self, pairs, ratings):
        return None

    def get_params(self, deep = True):
        pass