from lenskit.algorithms.basic import Random
from src.recommenders.recommender import Recommender
from src.utils import process_parameters
import pandas as pd


class RandomItem(Recommender):
    def __init__(self, parameters: dict) -> None:
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)
        self.parameters = parameters
        self.random_item = Random()

    def fit(self, ratings: pd.DataFrame, **kwargs):
        self.random_item.fit(ratings)

    def recommend(self, users, n, candidates, ratings):
        return self.random_item.recommend(users, n, candidates, ratings)

    def predict_for_user(self, user, items, ratings):
        raise Exception("RandomItem - predict_for_user não foi implementado")

    def predict(self, pairs, ratings):
        raise Exception("RandomItem - predict não foi implementado")

    def get_params(self, deep = True):
        raise Exception("RandomItem - get_params não foi implementado")
