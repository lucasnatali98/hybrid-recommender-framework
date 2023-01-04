from src.recommenders.recommender import Recommender
from src.utils import process_parameters
from lenskit.algorithms.basic import PopScore as PopScoreLenskit
import pandas as pd
class PopScore(Recommender):
    def __init__(self, parameters: dict) -> None:
        """

        """
        default_keys = {
            'maxNumberNeighbors',
            'minNumberNeighbors',
            'saveNeighbors',
            'feedback'
        }
        parameters = process_parameters(parameters, default_keys)



        self.PopScore = PopScoreLenskit()


    def predict_for_users(self, users, items, ratings):
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

    def recommend(self, users, n, candidates, ratings) -> pd.DataFrame:
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