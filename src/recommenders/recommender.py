
from abc import abstractmethod
from src.recommenders.algorithm import Algorithm


class Recommender(Algorithm):

    @abstractmethod
    def recommend(self, algorithm, users, n, candidates, ratings):
        """

        @param n:
        @param candidates:
        @param ratings:
        @return:
        """
        pass

    @abstractmethod
    def predict(self, pairs, ratings):
        """

        @param pairs:
        @param ratings:
        @return:
        """
        pass

    @abstractmethod
    def predict_for_users(self, users, items, ratings):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        pass

    def process_parameters(self, parameters: dict) -> dict:
        pass

    