import pandas as pd
from src.download import download_movielens
from src.data.dataset import AbstractDataSet
from src.utils import process_parameters, \
    create_directory, \
    hrf_data_storage_path, \
    check_if_directory_exists, check_if_directory_is_empty, unzip_file, hrf_build_path
PROPORTION_POSSIBILITIES = {
    "lastFM2",
}


def _is_proportion_valid(proportion) -> bool:
    if proportion in PROPORTION_POSSIBILITIES:
        return True

    return False


class LastFM2(AbstractDataSet):
    def __init__(self, parameters: dict) -> None:
        """
        @param proportion = qual a proporção do MovieLens vamos carregar
        """
        super().__init__()
        default_keys = {
            'proportion'
        }
        parameters = process_parameters(parameters, default_keys)
        proportion = parameters.get('proportion', 'lastFM2')

        if not _is_proportion_valid(proportion):
            raise Exception(
                "A proporção da base de dados está invalida, escolha por: [ lastFM2]"
            )

        self.config_obj = parameters
        self.filters = parameters.get('filters', None)
        self.proportion = proportion
        self.basePath = "academic\\bcc409\p2022_2\grupo3\\"
        self.dataset = self._get_dataset()
        self.genomeScores = None
        self.genomeTags = None

    def transform_columns_to_lenskit_pattern(self, dataset: pd.DataFrame) -> pd.DataFrame:
        dataset = dataset.rename(columns={
            "artistID": "item",
            "userID": "user",
            "weight": "rating",
        })
        return dataset

    def _load_lastFM2(self) -> str:

        response = ("success", "failure")
        path = self.basePath + "./"
        users = self.Loader.load_file(path=path + "user_artists_filtrado", extension=".csv")
        self.set_items(users)
        self.set_ratings(users)
        self.set_users(users)
        return response[0]


    def set_ratings(self, ratings):
        ratings = self.transform_columns_to_lenskit_pattern(ratings)
        setattr(LastFM2, 'ratings', ratings)
    def set_items(self, items):
        setattr(LastFM2, 'items', items)

    def set_users(self, users):
        setattr(LastFM2, 'users', users)


    def _get_dataset(self):
        load_result = None
        if self.proportion == "lastFM2":
            load_result = self._load_lastFM2()

        if load_result == "success":
            return [
                self.items,
                self.ratings,
            ]
        else:
            return None

    @property
    def ratings(self):
        return self.ratings


    @property
    def items(self):
        return self.items

    @property
    def users(self):
        return None
