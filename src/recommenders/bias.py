from src.recommenders.recommender import Recommender
from lenskit.algorithms import bias, Recommender as LenskitRecommender
from src.utils import process_parameters
import pandas as pd


class Bias(Recommender):
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


class LenskitBias(Bias):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

        self.items = parameters.get('items', True)
        self.users = parameters.get('users', True)
        self.damping = parameters.get('damping', 0.0)
        self.Bias = LenskitRecommender.adapt(bias.Bias(
            items=self.items,
            users=self.users,
        ))

    def predict_for_user(self, user, items, ratings):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        return self.Bias.predict_for_user(user, items, ratings)

    def predict(self, pairs, ratings):
        """

        @param pairs:
        @param ratings:
        @return:
        """
        return self.Bias.predict(pairs, ratings)

    def recommend(self,users, n, candidates=None, ratings=None) -> pd.DataFrame:
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
        self.Bias.fit(rating)

    def transform(self, rating):
        return self.Bias.transform(rating)
