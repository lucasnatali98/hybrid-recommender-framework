from lenskit.algorithms.basic import UnratedItemCandidateSelector

from src.recommenders.recommender import Recommender
from lenskit.algorithms import user_knn, Recommender as LenskitRecommender
from pandas import DataFrame
from lenskit.algorithms.ranking import TopN
from src.utils import process_parameters
from lenskit.algorithms.user_knn import UserUser
import pandas as pd



class UserKNN(Recommender):
    def __init__(self, parameters: dict) -> None:
        default_keys = {
            'maxNumberNeighbors',
            'minNumberNeighbors',
            'min_sim',
            'feedback'
        }
        parameters = process_parameters(parameters, default_keys)

        print("User KNN - parameters: ", parameters)
        self.max_number_neighbors = parameters['maxNumberNeighbors']
        self.min_number_neighbors = parameters['minNumberNeighbors']
        self.min_sim = parameters['min_sim']
        self.feedback = parameters['feedback']
        self.user_knn = user_knn.UserUser(
            nnbrs=self.max_number_neighbors,
           # min_nbrs=self.min_number_neighbors, #parâmetro dando problema
           # min_sim=self.min_sim,
           # feedback=self.feedback
        )



    def predict_for_user(self, user, items, ratings=None):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        return self.user_knn.predict_for_user(
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
        return self.user_knn.predict(
            pairs,
            ratings)

    def fit(self, ratings: DataFrame, **kwargs):
        """

        @param ratings:
        @param kwargs:
        @return:
        """
        return self.user_knn.fit(ratings)

    def recommend(self, algorithm, users, n=None, candidates=None, n_jobs=None):


        select = UnratedItemCandidateSelector()


        top_n = TopN(algorithm, select)


        for user in users:
            print("user: ", user)
            recs = top_n.recommend(
                user=user,
                n=10,
            )
            print("recs: ", recs)

        return ""

    def get_params(self, deep=True):
        pass
