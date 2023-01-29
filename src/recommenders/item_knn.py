from src.recommenders.recommender import Recommender
from lenskit.algorithms import item_knn, Recommender as LenskitRecommender
from lenskit.algorithms.ranking import TopN
from lenskit import batch
from src.utils import process_parameters
import pandas as pd


class ItemKNN(Recommender):
    def __init__(self, parameters: dict) -> None:
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)


class LenskitItemKNN(ItemKNN):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = {
            'maxNumberNeighbors',
            'minNumberNeighbors',
            'saveNeighbors',
            'feedback'
        }

        parameters = process_parameters(parameters, default_keys)
        self.max_number_neighbors = parameters.get('maxNumberNeighbors')
        self.min_number_neighbors = parameters.get('minNumberNeighbors')
        self.save_nbrs = parameters.get('saveNeighbors')
        self.feedback = parameters.get('feedback')
        self.aggregate = parameters.get('aggregate')
        self.use_ratings = parameters.get('use_ratings')

        self.ItemKNN = item_knn.ItemItem(
            nnbrs=self.max_number_neighbors,
            min_nbrs=self.min_number_neighbors,
            save_nbrs=self.save_nbrs,
            min_sim=0.03,
            feedback=self.feedback,
            aggregate=self.aggregate,
            use_ratings=self.use_ratings
        )
        self.ItemKNN = LenskitRecommender.adapt(self.ItemKNN)

    def predict_for_user(self, users, items, rating=None):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        return self.ItemKNN.predict_for_user(users, items, rating)

    def predict(self, pairs, ratings):
        """

        @param pairs:
        @param ratings:
        @return:
        """

        return self.ItemKNN.predict(pairs, ratings)

    def recommend(self, users, n, candidates=None, n_jobs=None) -> pd.DataFrame:
        """

        @param user:
        @param n:;
        @param candidates:
        @param ratings:
        @return:
        """

        print("ItemKNN recommend")
        recommendation_dataframe = pd.DataFrame(
            columns=['user', 'item', 'score', 'algorithm_name']
        )
        for user in users:
            recommendation_to_user = self.ItemKNN.recommend(user, n)

            names = pd.Series([self.__class__.__name__] * n)
            user_id_list = pd.Series([user] * n)

            recommendation_to_user['algorithm_name'] = names
            recommendation_to_user['user'] = user_id_list

            recommendation_dataframe = pd.concat(
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

    def fit(self, rating, **kwargs) -> None:
        """

        @param rating:
        @param kwargs:
        @return:
        """
        self.ItemKNN.fit(rating)
