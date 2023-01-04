from src.preprocessing.missing import MissingProcessing
from src.data.movielens import MovieLens

parameters_missing_processing = {

}
parameters_movielens = {
    'proportion': 'ml-latest-small',
    'filters': {}
}
missing_processing = MissingProcessing(parameters_missing_processing)
movielens = MovieLens(parameters_movielens)
ratings = movielens.ratings



class TestMissingProcessing:
    def test_pre_processing(self):

        missing_processing.pre_processing(ratings)