import pytest
from src.data.movielens import MovieLens
from src.recommenders.pop_score import PopScore

movielens = MovieLens({
    'proportion': 'ml-latest-small',
    'filters': {}
})

parameters = {
    'score_method': 'quantile'
}
pop_score = PopScore(parameters)


class TestPopScore:
    def test_fit(self):
        pass

    def test_recommend(self):
        pass

    def test_predict(self):
        pass

    def test_predict_for_users(self):
        pass

    def get_params(self):
        pass
