
from src.recommenders.recommender import Recommender
from src.utils import process_parameters
from lenskit.algorithms.basic import Memorized as MemorizedLenskit
from lenskit.algorithms import  Recommender as LenskitRecommender

from pandas import DataFrame, Series

class Memorized:
    def __init__(self, parameters: dict) -> None:
        default_keys = {
            'lib'
        }
        parameters = process_parameters(parameters, default_keys)
        self.lib = parameters.get('lib', 'lenskit')

        if self.lib == 'lenskit':
            self.fittable = MemorizedLenskit(parameters)



class MemorizedLenskit(Recommender):
    def __init__(self, parameters: dict) -> None:
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

        self.parameters = parameters
        self.Memorized = MemorizedLenskit(self.parameters['scores'])
        self.Memorized = LenskitRecommender.adapt(self.Memorized)

    def predict_for_user(self, user, items, ratings=None):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        return self.Memorized.predict_for_user(
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
        return self.Memorized.predict(
            pairs,
            ratings)

    def fit(self, ratings: DataFrame, **kwargs) -> None:
        return self.Memorized.fit(ratings)

    def recommend(self, users, n=None, candidates=None, n_jobs=None) -> pd.DataFrame:
        print("UserKNN recommend")
        recommendation_dataframe = DataFrame(
            columns=['user', 'item', 'score', 'algorithm_name']
        )
        for user in users:
            recommendation_to_user = self.Memorized.recommend(user, n)

            names = Series([self.__class__.__name__] * n)
            user_id_list = Series([user] * n)

            recommendation_to_user['algorithm_name'] = names
            recommendation_to_user['user'] = user_id_list

            recommendation_dataframe = pd.concat(
                [recommendation_dataframe, recommendation_to_user],
                ignore_index=True
            )

        return recommendation_dataframe

    def get_params(self, deep=True):
        pass
