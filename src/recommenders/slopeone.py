from src.recommenders.recommender import Recommender


class SlopeOne(Recommender):
    def __init__(self, parameters: dict) -> None:
        """
        
        """
        pass

    def predict_for_users(self, users, items, ratings):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        pass

    def predict(self, pairs, ratings):
        """

        @param pairs:
        @param ratings:
        @return:
        """
        pass

    def recommend(self, user, n, candidates, ratings):
        """

        @param user:
        @param n:
        @param candidates:
        @param ratings:
        @return:
        """
        pass

    def fit(self):
        """

        @return:
        """
        pass


    def get_params(self, deep = True):
        """

        @param deep:
        @return:
        """
        pass