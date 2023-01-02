import pytest
from src.data.movielens import MovieLens
from src.recommenders.user_knn import UserKNN

movielens = MovieLens({
    'proportion': 'ml-latest-small',
    'filters': {}
})

parameters = {
    "maxNumberNeighbors": 1,
    "minNumberNeighbors": 2,
    "min_sim": "",
    "feedback": "implicit",
    "aggregate": "weighted-average",
    "use_ratings": True
}
user_knn = UserKNN(parameters)


class TestUserKNN:
    def test_fit(self):
        pass

    def test_recommend(self):
        pass

    def test_predict(self):
        pass

    def test_predict_for_users(self):
        pass
