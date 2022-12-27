from src.recommenders.recommender import Recommender
from lenskit.algorithms import bias
from src.utils import process_parameters


class Bias(Recommender):
    def __init__(self, parameters: dict) -> None:
        default_keys = {'items', 'users', 'damping'}
        parameters = process_parameters(parameters, default_keys)

        self.items = parameters['items']
        self.users = parameters['users']
        self.damping = parameters['damping']
        self.Bias = bias.Bias(
            items=self.items,
            users=self.users,
        )

    def predict_for_users(self, users, items, ratings):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        return self.Bias.predict_for_user(users, items, ratings)

    def predict(self, pairs, ratings):
        """

        @param pairs:
        @param ratings:
        @return:
        """
        return self.Bias.predict(pairs, ratings)

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
        self.Bias.fit(rating)

    def transform(self, rating):
        return self.Bias.transform(rating)
