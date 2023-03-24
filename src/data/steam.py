from docutils.nodes import entry
from src.data.dataset import AbstractDataSet
import pandas as pd
from src.utils import hrf_data_storage_path

class steamDB(AbstractDataSet):
    def __init__(self, parameters: dict) -> None:
        super().__init__()
        self.steamDB_path = hrf_data_storage_path().joinpath("steam")

        self.datasets = self.load_datasets()


    def load_datasets(self):
        ratings = pd.read_csv(self.steamDB_path.joinpath("ratings.csv"),sep=',')
        items = pd.read_csv(self.steamDB_path.joinpath("items.csv"),sep=',')
        users = pd.read_csv(self.steamDB_path.joinpath("users.csv"),sep=',')
        ratings = self.convert_to_hrf_pattern(ratings)

        self.set_ratings(ratings)
        self.set_items(items)
        self.set_users(users)


    def convert_to_hrf_pattern(self, rating: pd.DataFrame):
        rating = rating.rename(columns={
            "user_id": "user",
            "rating": "rating",
            "game_id": "item"
        })
        print(rating)
        return rating

    def set_users(self, users):
        setattr(steamDB, 'users', users)

    def set_items(self, items):
        setattr(steamDB, 'items', items)

    def set_ratings(self, ratings):
        setattr(steamDB, 'ratings', ratings)

    @property
    def items(self):
        return self.items
    @property
    def ratings(self):
        return self.ratings
    @property
    def users(self):
        return self.users
