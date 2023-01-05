from src.recommenders.recommender import Recommender
from surprise import SlopeOne as SlopeOneSurprise
from src.utils import process_parameters

class SlopeOne(Recommender):
    def __init__(self, parameters: dict) -> None:
        """
        
        """
        default_keys = set()
        parameters = process_parameters(parameters);
        self.slope_one = SlopeOneSurprise()


    def predict_for_users(self, users, items, ratings):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        raise Exception("O método não está implementado para essa classe")

    def predict(self, pairs, ratings):
        """

        @param pairs:
        @param ratings:
        @return:
        """
        return

    def recommend(self, users, n, candidates, ratings):
        """

        @param user:
        @param n:
        @param candidates:
        @param ratings:
        @return:
        """
        return None


    def fit(self, data, **kwargs):
        """

        @return:
        """
        return self.slope_one.fit(data)


    def get_params(self, deep = True):
        """

        @param deep:
        @return:
        """
        pass