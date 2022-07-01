
from abc import abstractmethod
from recommenders.algorithm import Algorithm


class Recommender(Algorithm):

    @abstractmethod
    def recommend(user, n, candidates, ratings):
        """
        
        """
        pass

    @abstractmethod
    def predict(pairs, ratings):
        """
        
        """
        pass

    @abstractmethod
    def predict_for_users(users, itens, ratings):
        """
        
        """
        pass

    