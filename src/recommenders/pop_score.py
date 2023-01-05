from src.recommenders.recommender import Recommender
from src.utils import process_parameters
from lenskit.algorithms import Recommender as LenskitRecommender
from lenskit.algorithms.basic import PopScore as PopScoreLenskit
from pandas import DataFrame, Series


class PopScore(Recommender):
    def __init__(self, parameters: dict) -> None:
        """

        """
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

        self.PopScore = PopScoreLenskit()
        self.PopScore = LenskitRecommender.adapt(self.PopScore)

    def predict_for_user(self, user, items, ratings=None):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        return self.PopScore.predict_for_user(user, items, ratings)

    def predict(self, pairs: DataFrame, ratings):
        """

        @param pairs:
        @param ratings:
        @return:
        """
        return self.PopScore.predict(pairs, ratings)

    def recommend(self, user, n, candidates = None, ratings = None) -> DataFrame:
        """

        @param user:
        @param n:
        @param candidates:
        @param ratings:
        @return:
        """
        return self.PopScore.recommend(user, n)

    def get_params(self, deep=True):
        """

        @param deep:
        @return:
        """
        pass

    def fit(self, rating: DataFrame, **kwargs):
        """

        @param rating:
        @param kwargs:
        @return:
        """
        self.PopScore.fit(rating)
