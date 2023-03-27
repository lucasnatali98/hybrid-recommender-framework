from src.data.movielens import MovieLens
from src.data.loader import Loader
from src.utils import hrf_external_path
from src.preprocessing.normalize import NormalizeProcessing
metric_calculator_path = hrf_external_path().joinpath("metric_calculator")

loader = Loader()
normalizer = NormalizeProcessing({
    'norm': 'l2'
})
ratings = MovieLens({
    'proportion': 'ml-latest-small'
}).ratings
ratings.drop(columns=['timestamp'], inplace=True)

loader.convert_to_text(ratings, metric_calculator_path.joinpath("ratings-movielens.txt"))

ratings_normalized = normalizer.pre_processing(ratings)
loader.convert_to_text(ratings_normalized,
                       metric_calculator_path.joinpath("ratings-movielens-normalized.txt"))
