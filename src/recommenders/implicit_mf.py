from src.recommenders.recommender import Recommender
from lenskit.algorithms.als import ImplicitMF as ImplicitMFLenskit
from lenskit.algorithms import Recommender as LenskitRecommender
from src.utils import process_parameters
import pandas as pd


class ImplicitMF(Recommender):

    def __init__(self, parameters: dict) -> None:
        default_keys = {
            "features",
            "iterations"
        }
        parameters = process_parameters(parameters, default_keys)
        self.features = parameters['features']
        self.iterations = parameters['iterations']
       # self.reg = parameters['reg']  # regularization factor
       # self.weight = parameters['weight']
       # self.use_ratings = parameters['use_ratings']
        self.ImplicitMF = ImplicitMFLenskit(
            features=self.features,
            iterations=self.iterations
        )

        self.ImplicitMF = LenskitRecommender.adapt(self.ImplicitMF)

    def predict_for_user(self, user, items, ratings=None):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        self.ImplicitMF.predict_for_user(user, items, ratings)

    def predict(self, pairs, ratings):
        """

        @param pairs:
        @param ratings:
        @return:
        """
        return self.ImplicitMF.predict(pairs, ratings)

    def recommend(self, user, n, candidates = None, ratings = None) -> pd.DataFrame:
        """

        @param user:
        @param n:
        @param candidates:
        @param ratings:
        @return:
        """
        return self.ImplicitMF.recommend(user, n)

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

        self.ImplicitMF.fit(rating)
