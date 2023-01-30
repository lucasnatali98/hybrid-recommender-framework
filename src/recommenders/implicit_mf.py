import traceback
from src.recommenders.recommender import Recommender
from lenskit.algorithms.als import ImplicitMF as ImplicitMFLenskitAlgorithm
from lenskit.algorithms import Recommender as LenskitRecommender
from src.utils import process_parameters
from pandas import DataFrame, Series, concat


class ImplicitMF(Recommender):
    def __init__(self, parameters: dict) -> None:
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)


class LenskitImplicitMF(ImplicitMF):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = {
            "features",
            "iterations"
        }
        parameters = process_parameters(parameters, default_keys)
        self.features = parameters.get('features')  # int
        self.iterations = parameters.get('iterations')  # int

        self.ImplicitMF = ImplicitMFLenskitAlgorithm(
            features=self.features,
            iterations=self.iterations
        )#reg,weight, use_ratings

        self.ImplicitMF = LenskitRecommender.adapt(self.ImplicitMF)

    def predict_for_user(self, user, items, ratings=None):
        return self.ImplicitMF.predict_for_user(user, items, ratings)

    def predict(self, pairs, ratings):
        return self.ImplicitMF.predict(pairs, ratings)

    def recommend(self, users, n, candidates=None, ratings=None):
        try:
            recommendation_dataframe = DataFrame(
                columns=['user', 'item', 'score', 'algorithm_name']
            )
            for user in users:
                recommendation_to_user = self.ImplicitMF.recommend(user, n)

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
            print("Aconteceu uma exceção na função recommend de ImplicitMF")
            print("Error: ", e)
            print(traceback.print_exc())
            return None

    def get_params(self, deep=True):
        pass

    def fit(self, rating, **kwargs) -> None:
        self.ImplicitMF.fit(rating)
