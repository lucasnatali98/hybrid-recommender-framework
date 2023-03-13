from docutils.nodes import entry
from src.data.dataset import AbstractDataSet
import pandas as pd
from src.utils import hrf_data_storage_path

class BookCrossing(AbstractDataSet):
    def __init__(self, parameters: dict) -> None:
        super().__init__()
        self.book_crossing_path = hrf_data_storage_path().joinpath("book-crossing")

        self.datasets = self.load_datasets()


    def load_datasets(self):
        ratings = pd.read_csv(self.book_crossing_path.joinpath("BX-Book-Ratings.csv"),sep=';', encoding='unicode_escape', error_bad_lines=False)
        books = pd.read_csv(self.book_crossing_path.joinpath("BX-Books.csv"),sep=';', encoding='unicode_escape', error_bad_lines=False)
        users = pd.read_csv(self.book_crossing_path.joinpath("BX-Users.csv"),sep=';', encoding='unicode_escape', error_bad_lines=False)
        ratings = self.convert_to_hrf_pattern(ratings)

        self.set_ratings(ratings)
        self.set_items(books)
        self.set_users(users)


    def convert_to_hrf_pattern(self, rating: pd.DataFrame):
        rating = rating.rename(columns={
            "User-ID": "user",
            "Book-Rating": "rating"
        })
        print(rating)
        return rating

    def set_users(self, users):
        setattr(BookCrossing, 'users', users)

    def set_items(self, items):
        setattr(BookCrossing, 'items', items)

    def set_ratings(self, ratings):
        setattr(BookCrossing, 'ratings', ratings)

    @property
    def items(self):
        return self.items
    @property
    def ratings(self):
        return self.ratings
    @property
    def users(self):
        return self.users
