from src.relevance import Relevance
from src.data.movielens import MovieLens

movielens = MovieLens({
    'proportion': 'ml-latest-small'
})
relevance = Relevance(3)
ratings = movielens.ratings


class TestRelevance:

    def test_select_ratings_by_relevance(self):
        print("test_select_ratings_by_relevance")
        new_ratings = relevance.select_ratings_by_relevance(ratings, 4.0)
        print(new_ratings)

    def test_most_popular_item(self):
        print("test most popular item")
        popular_items_to_user = relevance.most_popular_item(ratings, 1)
        print(popular_items_to_user)

    def test_most_popular_items(self):
        popular_items = relevance.most_popular_items(ratings)
        print(popular_items)
