import pandas as pd
from src.data.dataset import AbstractDataSet
from src.utils import process_parameters,\
    create_directory,\
    hrf_data_storage_path,\
    check_if_directory_exists, check_if_directory_is_empty, unzip_file, hrf_build_path

PROPORTION_POSSIBILITIES = {
    "ml-25m",
    "ml-latest",
    "ml-latest-small",
}


def _is_proportion_valid(proportion) -> bool:
    if proportion in PROPORTION_POSSIBILITIES:
        return True

    return False


class MovieLens(AbstractDataSet):
    def __init__(self, parameters: dict) -> None:
        """
        @param proportion = qual a proporção do MovieLens vamos carregar
        """
        super().__init__()
        default_keys = {
            'proportion'
        }
        parameters = process_parameters(parameters, default_keys)
        proportion = parameters.get('proportion', 'ml-latest-small')

        if not _is_proportion_valid(proportion):
            raise Exception(
                "A proporção da base de dados está invalida, escolha por: [ ml-25m, ml-latest, ml-latest-small]"
            )

        self.config_obj = parameters
        self.filters = parameters.get('filters', None)
        self.proportion = proportion
        self.basePath = "data_storage/"
        self.dataset = self._get_dataset()
        self.genomeScores = None
        self.genomeTags = None

    def transform_columns_to_lenskit_pattern(self, dataset: pd.DataFrame) -> pd.DataFrame:
        dataset = dataset.rename(columns={
            "movieId": "item",
            "userId": "user",
        })
        return dataset

    def _load_ml25m(self) -> None:
        """


        """

        path = self.basePath + "ml-25m/"
        movies = self.Loader.load_file(path=path + "movies", extension=".csv")
        links = self.Loader.load_file(path=path + "links", extension=".csv")
        ratings = self.Loader.load_file(path=path + "ratings", extension=".csv")
        tags = self.Loader.load_file(path=path + "tags", extension=".csv")
        genome_scores = self.Loader.load_file(path=path + "genome-scores", extension=".csv")
        genome_tags = self.Loader.load_file(path=path + "genome-tags", extension=".csv")

        self.set_items(movies)
        self.set_tags(tags)
        self.set_ratings(ratings)
        self.set_links(links)
        self.set_genome_tags(genome_tags)
        self.set_genome_scores(genome_scores)

    def _load_ml_latest(self) -> None:
        """

        """
        path = self.basePath + "ml-latest/"
        movies = self.Loader.load_file(path=path + "movies", extension=".csv")
        links = self.Loader.load_file(path=path + "links", extension=".csv")
        ratings = self.Loader.load_file(path=path + "ratings", extension=".csv")
        tags = self.Loader.load_file(path=path + "tags", extension=".csv")
        genome_scores = self.Loader.load_file(path=path + "genome-scores", extension=".csv")
        genome_tags = self.Loader.load_file(path=path + "genome-tags", extension=".csv")

        self.set_items(movies)
        self.set_tags(tags)
        self.set_ratings(ratings)
        self.set_links(links)
        self.set_genome_tags(genome_tags)
        self.set_genome_scores(genome_scores)

    def _load_ml_latest_small(self) -> str:
        """


        """
        response = ("success", "failure")
        ml_latest_small_path = hrf_data_storage_path().joinpath("ml-latest-small")
        ml_latest_small_zip_file = hrf_build_path().joinpath("ml-latest-small.zip")

        is_ml_latest_small_path_exists = check_if_directory_exists(ml_latest_small_path)
        is_ml_latest_small_empty = check_if_directory_is_empty(hrf_data_storage_path(), "ml-latest-small")

        if is_ml_latest_small_path_exists and is_ml_latest_small_empty is False:
            path = self.basePath + "ml-latest-small/"
            movies = self.Loader.load_file(path=path + "movies", extension=".csv")
            links = self.Loader.load_file(path=path + "links", extension=".csv")
            ratings = self.Loader.load_file(path=path + "ratings", extension=".csv")
            tags = self.Loader.load_file(path=path + "tags", extension=".csv")

            self.set_items(movies)
            self.set_tags(tags)
            self.set_ratings(ratings)
            self.set_links(links)
            return response[0]
        else:
            c = create_directory(hrf_data_storage_path(), "ml-latest-small")

            if c is None:
                raise Exception("Não foi possivel criar o diretório - ml-latest-small")

            print("O diretório (ml-latest-small) foi criado com sucesso")
            print("Extraindo os arquivos...")
            unzip_file(path_to_zip_file=ml_latest_small_zip_file, path_to_extract=hrf_data_storage_path())

            path = self.basePath + "ml-latest-small/"
            movies = self.Loader.load_file(path=path + "movies", extension=".csv")
            links = self.Loader.load_file(path=path + "links", extension=".csv")
            ratings = self.Loader.load_file(path=path + "ratings", extension=".csv")
            tags = self.Loader.load_file(path=path + "tags", extension=".csv")

            self.set_items(movies)
            self.set_tags(tags)
            self.set_ratings(ratings)
            self.set_links(links)
            return response[0]


    def set_ratings(self, ratings):
        ratings = self.transform_columns_to_lenskit_pattern(ratings)
        setattr(MovieLens, 'ratings', ratings)

    def set_links(self, links):
        setattr(MovieLens, 'links', links)

    def set_items(self, items):
        setattr(MovieLens, 'items', items)

    def set_users(self, users):
        setattr(MovieLens, 'users', users)

    def set_tags(self, tags):
        setattr(MovieLens, 'tags', tags)

    def set_genome_tags(self, genome_tags):
        setattr(MovieLens, 'genomeTags', genome_tags)

    def set_genome_scores(self, genome_scores):
        setattr(MovieLens, 'genomeScores', genome_scores)

    def apply_filters(self):
        filters = self.config_obj['filters']

        if filters is None:
            return self.ratings

        if not filters:
            return self.ratings

        qtd_ratings = filters['qtd_ratings']
        new_ratings = self.ratings[0:qtd_ratings]
        return new_ratings

    def _get_dataset(self):
        """

        @return:
        """
        load_result = None
        if self.proportion == "ml-25m":
            load_result = self._load_ml25m()
        if self.proportion == "ml-latest":
            load_result = self._load_ml_latest()
        if self.proportion == "ml-latest-small":
            load_result = self._load_ml_latest_small()

        if load_result == "success":
            return [
                self.items,
                self.links,
                self.ratings,
                self.tags,
            ]
        else:
            return None

    @property
    def ratings(self):
        return self.ratings

    @property
    def tags(self):
        return self.tags

    @property
    def links(self):
        return self.links

    @property
    def items(self):
        return self.items

    @property
    def users(self):
        return None
