import pytest
from src.data.movielens import MovieLens
from src.visualization.static_bar import StaticBar
movielens = MovieLens(
    {
        'proportion': 'ml-latest-small',
        'filters': {}
    }
)
ratings = movielens.ratings

parameters = {
    'plot_types': {
        "ratings_by_user": True,
        "ratings_by_movie": True,
        "items_predict": True,
        "movie_ratings_distribution": True
    }
}

class TestStaticBar:

    def test_plot(self):
        pass

    def test_ratings_by_user_plot(self):
        static_bar = StaticBar(parameters)
        static_bar.ratings_by_user_plot(ratings)

    def test_ratings_by_movie_plot(self):
        static_bar = StaticBar(parameters)
        static_bar.ratings_by_movie_plot(ratings)