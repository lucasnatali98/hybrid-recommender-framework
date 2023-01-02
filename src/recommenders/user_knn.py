from src.recommenders.recommender import Recommender
from lenskit.algorithms import user_knn, Recommender as LenskitRecommender
from pandas import DataFrame
from lenskit.algorithms.ranking import TopN
from src.utils import process_parameters
from lenskit import batch


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
            min_nbrs=self.min_number_neighbors,
            min_sim=self.min_sim,
            feedback=self.feedback
        )


    def predict_for_user(self, user, items, ratings=None):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        print("Predict for user - user knn")
        print("ratings: ", ratings)
        return self.user_knn.predict_for_user(
            user,
            items,
            ratings
        )

    def predict(self, user, items, ratings=None):
        """

        @param user:
        @param items:
        @return:
        """
        return self.user_knn.predict_for_user(
            user,
            items,
            ratings
        )

    def fit(self, ratings: DataFrame, **kwargs):
        """

        @param ratings:
        @param kwargs:
        @return:
        """
        self.user_knn.fit(ratings)

    def recommend(self, algorithm, users, n=None, candidates=None, n_jobs=None):
        print("Item KNN - recommend function")
        print('algorithm: ', algorithm)
        print('users: ', users)
        print('n: ', n)
        print('candidates: ', candidates)
        print('n_jobs: ', n_jobs)
        print('\n')
        algorithm = LenskitRecommender.adapt(algorithm)
        recs = batch.recommend(algorithm, users, n)
        print("recs: ", recs)
        return recs

    def get_params(self, deep=True):
        pass
