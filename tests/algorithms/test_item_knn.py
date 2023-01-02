import pytest
from src.data.movielens import MovieLens
from src.recommenders.item_knn import ItemKNN

movielens = MovieLens({
    'proportion': 'ml-latest-small',
    'filters': {}
})

parameters = {
    "maxNumberNeighbors": 1,
    "minNumberNeighbors": 2,
    "saveNeighbors": 3.0,
    "feedback": "implicit",
    "aggregate": "weighted-average",
    "use_ratings": True
}
item_knn = ItemKNN(parameters)


class TestItemKNN:
    def test_fit(self):
        pass

    def test_recommend(self):
        pass

    def test_predict(self):
        pass

    def test_predict_for_users(self):
        pass
