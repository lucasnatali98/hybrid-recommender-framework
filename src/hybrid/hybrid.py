
from src.recommenders.recommender import Recommender
from pandas import DataFrame, Series

class Hybrid: #Deve herdar de quem?

    def __init__(self, parameters: dict) -> None:
        self.constituent_algorithm = []
        self.metafeatures = []


    def add_metafeature(self, metafeature) -> None:
        """

        @param metafeature:
        @return:
        """
        self.metafeatures.append(metafeature)


    def remove_metafeature(self, metafeature):
        """

        @param metafeature:
        @return:
        """
        self.metafeatures.remove(metafeature)
    def add_algorithm(self, algorithm) -> None:
        """
        
        """
        self.constituent_algorithm.append(algorithm)
    def remove_algorithm(self, algorithm) -> None:
        """
        
        """
        self.remove_algorithm(algorithm)

    def combine_user_metafeature_with_predictions(self, metafeature: DataFrame, predictions: DataFrame) -> DataFrame:
        pass

    def combine_item_metafeature_with_predictions(self, metafeature: DataFrame, predictions: DataFrame) -> DataFrame:
        pass

    def combine_user_item_metafeature_with_predictions(self, metafeature: DataFrame, predictions: DataFrame) -> DataFrame:
        pass


    def predict_new_score(self):
        pass