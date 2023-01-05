from src.recommenders.recommender import Recommender
from src.utils import process_parameters
from lenskit.algorithms import Recommender as LenskitRecommender
from lenskit.algorithms.basic import PopScore as PopScoreLenskit
from pandas import DataFrame, Series, concat


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

    def recommend(self, users, n, candidates = None, ratings = None) -> DataFrame:
        """

        @param user:
        @param n:
        @param candidates:
        @param ratings:
        @return:
        """
        print("PopScore - recommend")
        recommendation_dataframe = DataFrame(
            columns=['user', 'item', 'score', 'algorithm_name']
        )
        for user in users:
            recommendation_to_user = self.PopScore.recommend(user, n)

            names = Series([self.__class__.__name__] * n)
            user_id_list = Series([user] * n)

            recommendation_to_user['algorithm_name'] = names
            recommendation_to_user['user'] = user_id_list

            recommendation_dataframe = concat(
                [recommendation_dataframe, recommendation_to_user],
                ignore_index=True
            )

        return recommendation_dataframe

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
