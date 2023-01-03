from abc import abstractmethod
import pandas as pd
from src.recommenders.algorithm import Algorithm


class Recommender(Algorithm):

    @abstractmethod
    def recommend(self, users, n, candidates, ratings) -> pd.DataFrame:
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
    def predict_for_user(self, user, items, ratings):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        pass


    