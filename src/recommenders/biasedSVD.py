import traceback
from src.recommenders.recommender import Recommender
from src.utils import process_parameters
from pandas import DataFrame, Series, concat
from lenskit.algorithms.als import BiasedMF
from lenskit.algorithms import Recommender as LenskitRecommender


class BiasedSVD(Recommender):
    def __init__(self, parameters: dict) -> None:
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

class BiasedSVDLenskit(Recommender):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = {
            'iterations',
            'features'
        }

        parameters = process_parameters(parameters, default_keys)

        self.features = parameters.get('features')
        self.damping = parameters.get('damping')
        self.BiasedMF = BiasedMF(
            features=self.features,
            iterations=20
        )
        self.BiasedMF = LenskitRecommender.adapt(self.BiasedMF)

    def predict_for_user(self, user, items, ratings=None):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """

        return self.BiasedMF.predict_for_user(user,items,ratings)

    def predict(self, pairs, ratings):
        """

        @param pairs:
        @param ratings:
        @return:
        """
        return self.BiasedMF.predict(pairs, ratings)

    def recommend(self, users, n, candidates=None, ratings=None):
        """

        @param user:
        @param n:
        @param candidates:
        @param ratings:
        @return:
        """
        try:
            recommendation_dataframe = DataFrame(
                columns=['user', 'item', 'score', 'algorithm_name']
            )
            for user in users:
                recommendation_to_user = self.BiasedMF.recommend(user, n)

                names = Series([self.__class__.__name__] * n)
                user_id_list = Series([user] * n)

                recommendation_to_user['algorithm_name'] = names
                recommendation_to_user['user'] = user_id_list

                recommendation_dataframe = concat(
                    [recommendation_dataframe, recommendation_to_user],
                    ignore_index=True
                )

            return recommendation_dataframe
        except Exception as e:
            print("Uma exceção aconteceu na função recommnd de BiasedSVD")
            print("Error: ", e)
            print(traceback.print_exc())
            return None


    def get_params(self, deep=True):
        """

        @param deep:
        @return:
        """
        pass

    def fit(self, rating, **kwargs) -> None:
        """

        @param rating:
        @param kwargs:
        @return:
        """
        self.BiasedMF.fit(rating)
