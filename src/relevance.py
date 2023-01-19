import pandas as pd


class Relevance:
    def __init__(self, factor: int):
        self.factor = factor

    def select_ratings_by_relevance(self, database: pd.DataFrame, factor: float):
        pass

    def most_popular_item(self, database: pd.DataFrame, user_id):
        filtered_database = database.loc[database['user'] == user_id]
        print("filtered database")
        print(filtered_database)

        items = self._get_items(filtered_database)
        self._define_value_counts(items)

    def _get_items(self, database: pd.DataFrame) -> pd.Series:
        items = database.get('item', None)
        if items is None:
            raise Exception("")

        return items

    def _define_value_counts(self, items: pd.Series):
        items_value_counts = items.value_counts()
        return items_value_counts

    def most_popular_items(self, database: pd.DataFrame):
        items = self._get_items(database)
        return self._define_value_counts(items)
