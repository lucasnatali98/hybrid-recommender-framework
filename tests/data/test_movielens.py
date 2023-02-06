from src.data.movielens import MovieLens
import pytest
import pandas as pd


class TestMovielens:

    def test_transform_columns_to_lenskit_pattern(self):
        movielens = MovieLens({
            'proportion': 'ml-latest-small',
            'filters': {}
        })

        ratings = movielens.ratings

        ratings = movielens.transform_columns_to_lenskit_pattern(ratings)
        ratings_dataset_columns = ratings.columns

        lenskit_pattern_keys_set = {'user', 'item', 'rating'}
        ratings_keys_set = set()

        for column_name in ratings_dataset_columns:
            ratings_keys_set.add(column_name)

        assert lenskit_pattern_keys_set.issubset(ratings_keys_set) == True

    def test_ratings(self):
        movielens = MovieLens({
            'proportion': 'ml-latest-small',
            'filters': {}
        })

        ratings = movielens.ratings

        assert isinstance(ratings, pd.DataFrame) == True



    def test_items(self):
        movielens = MovieLens({
            'proportion': 'ml-latest-small',
            'filters': {}
        })

        items = movielens.items

        assert isinstance(items, pd.DataFrame) == True

    def test_tags(self):
        movielens = MovieLens({
            'proportion': 'ml-latest-small',
            'filters': {}
        })

        tags = movielens.tags

        assert isinstance(tags, pd.DataFrame) == True


