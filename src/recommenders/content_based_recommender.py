from src.recommenders.recommender import Recommender
from lenskit.algorithms import Recommender as LenskitRecommender
from src.utils import process_parameters
from pandas import DataFrame, Series


class ContentBasedRecommender(Recommender):
    def __init__(self, parameters: dict) -> None:
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def predict_for_user(self, user, items, ratings=None):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        pass

    def predict(self, pairs, ratings):
        """

        @param user:
        @param items:
        @return:
        """
        pass

    def fit(self, ratings: DataFrame, **kwargs):
        """

        @param ratings:
        @param kwargs:
        @return:
        """
        pass

    def recommend(self, users, n=None, candidates=None, n_jobs=None) -> DataFrame:
        pass

    def get_params(self, deep=True):
        pass
