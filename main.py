from src.data.loader import Loader
from src.data.movielens import MovieLens

movie_lens_dataset = MovieLens("ml-latest-small")

print(movie_lens_dataset.rating)


