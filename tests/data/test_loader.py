from src.data.loader import Loader
from src.data.movielens import MovieLens
from src.utils import hrf_experiment_output_path
from src.preprocessing.normalize import NormalizeProcessing

metrics_calculator_path = hrf_experiment_output_path().joinpath("datasets/metrics_calculator/")
loader = Loader()

movielens = MovieLens({
    'proportion': 'ml-latest-small'
})
ratings = movielens.ratings
normalize_process = NormalizeProcessing({
    'norm': 'l2',
    'axis': 0,
    'copy': True,
    'return_norm': False
})



class TestLoader:

    def test_convert_to(self):
        pass

    def test_convert_to_text(self):
        ratings.drop(columns=['timestamp'], inplace=True)

        ratings_normalized = normalize_process.pre_processing(ratings)
        print(ratings_normalized)
        ratings_path = metrics_calculator_path.joinpath("ratings.txt")
        ratings_norm_path = metrics_calculator_path.joinpath("ratingsNorm.txt")
        loader.convert_to_text(ratings, ratings_path)
        loader.convert_to_text(ratings_normalized, ratings_norm_path)
