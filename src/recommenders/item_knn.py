from src.recommenders.recommender import Recommender
from lenskit.algorithms import item_knn, Recommender as LenskitRecommender
from lenskit.algorithms.ranking import TopN
from lenskit import batch
from src.utils import process_parameters


class ItemKNN(Recommender):
    def __init__(self, parameters: dict) -> None:
        default_keys = {
            'maxNumberNeighbors',
            'minNumberNeighbors',
            'saveNeighbors',
            'feedback'
        }

        parameters = process_parameters(parameters, default_keys)
        self.max_number_neighbors = parameters['maxNumberNeighbors']
        self.min_number_neighbors = parameters['minNumberNeighbors']
        self.save_nbrs = parameters['saveNeighbors']
        self.feedback = parameters['feedback']
        self.aggregate = parameters['aggregate']
        self.use_ratings = parameters['use_ratings']


        print("Item KNN - parameters: ", parameters)
        self.ItemKNN = item_knn.ItemItem(
            nnbrs=self.max_number_neighbors,
            min_nbrs=self.min_number_neighbors,
            save_nbrs=self.save_nbrs,
            min_sim=0.0003,
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

    def recommend(self, algorithm, users, n, candidates=None, n_jobs=None):
        """

        @param user:
        @param n:;
        @param candidates:
        @param ratings:
        @return:
        """
        print("Item KNN - recommend function")
        print('algorithm: ', algorithm)
        print('users: ', users)
        print('n: ', n)
        print('candidates: ', candidates)
        print('n_jobs: ', n_jobs)
        print('\n')
        algorithm = LenskitRecommender.adapt(algorithm)
        recs = batch.recommend(algorithm, users, n)
        return recs

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
        self.ItemKNN.fit(rating)
