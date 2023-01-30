import traceback

from src.recommenders.recommender import Recommender
from src.utils import process_parameters
from lenskit.algorithms.svd import BiasedSVD
from lenskit.algorithms import Recommender as LenskitRecommender
import pandas as pd


class ScikitSVD(Recommender):
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


class LenskitScikitSVD(ScikitSVD):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = {
            "features"
        }
        parameters = process_parameters(parameters, default_keys)

        self.features = parameters.get('features')
        self.damping = parameters.get('damping')
        # self.bias = parameters['bias']  # regularization factor
        # self.algorithm = parameters['algorithm']

        self.BiasedSVD = BiasedSVD(
            features=self.features,
            damping=self.damping,
        )

        self.BiasedSVD = LenskitRecommender.adapt(self.BiasedSVD)

    def predict_for_user(self, user, items, ratings=None):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        return self.BiasedSVD.predict_for_user(
            user,
            items,
            ratings
        )

    def predict(self, pairs, ratings):
        """

        @param user:
        @param items:
        @return:
        """
        return self.BiasedSVD.predict(
            pairs,
            ratings)

    def fit(self, ratings: pd.DataFrame, **kwargs) -> None:
        """

        @param ratings:
        @param kwargs:
        @return:
        """
        self.BiasedSVD.fit(ratings)

    def recommend(self, users, n=None, candidates=None, n_jobs=None):
        print("ScikitSVD recommend")

        try:
            recommendation_dataframe = pd.DataFrame(
                columns=['user', 'item', 'score', 'algorithm_name']
            )
            for user in users:
                recommendation_to_user = self.BiasedSVD.recommend(user, n)

                names = pd.Series([self.__class__.__name__] * n)
                user_id_list = pd.Series([user] * n)

                recommendation_to_user['algorithm_name'] = names
                recommendation_to_user['user'] = user_id_list

                recommendation_dataframe = pd.concat(
                    [recommendation_dataframe, recommendation_to_user],
                    ignore_index=True
                )

            return recommendation_dataframe
        except Exception as e:
            print("Aconteceu uma exceção na função recommend de ScikitSVD")
            print("Error: ", e)
            print(traceback.print_exc())
            return None

    def get_params(self, deep=True):
        pass