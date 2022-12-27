from src.data.dataset import AbstractDataSet
from src.utils import process_parameters

PROPORTION_POSSIBILITIES = {
    "ml-25m",
    "ml-latest",
    "ml-latest-small",
}



class MovieLens(AbstractDataSet):
    """

    """

    def __init__(self, parameters: dict) -> None:
        """
        @param proportion = qual a proporção do MovieLens vamos carregar



        """
        super().__init__()
        default_keys = {
            'proportion'
        }
        proportion = str(parameters['proportion'])

        if not self._is_proportion_valid(proportion):
            raise Exception(
                "A proporção da base de dados está invalida, escolha por: [ ml-25m, ml-latest, ml-latest-small]"
            )

        parameters = process_parameters(parameters, default_keys)

        self.config_obj = parameters
        self.filters = parameters['filters']

        self.proportion = proportion
        self.basePath = "data_storage/"
        self.dataset = self._get_dataset()
        self.genomeScores = None
        self.genomeTags = None

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters: objeto com os parâmetros da classe
        @return: dicionário atualizado com esses mesmos parâmetros
        """

        parameters_keys_list = list(parameters.keys())

        parameters_keys = set()
        for parameter in parameters_keys_list:
            parameters_keys.add(parameter)

        if default_keys.issubset(parameters_keys):
            pass
        else:
            raise KeyError("Você não informou uma das chaves obrigatorias")
        return parameters

    def _is_proportion_valid(self, proportion) -> bool:
        """
        Check if the proportion of movielens dataset is valid

        @proportion: str

        """
        if proportion in PROPORTION_POSSIBILITIES:
            return True

        return False

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

    def _load_ml_latest_small(self) -> None:
        """


        """
        path = self.basePath + "ml-latest-small/"
        movies = self.Loader.load_file(path=path + "movies", extension=".csv")
        links = self.Loader.load_file(path=path + "links", extension=".csv")
        ratings = self.Loader.load_file(path=path + "ratings", extension=".csv")
        tags = self.Loader.load_file(path=path + "tags", extension=".csv")

        self.set_items(movies)
        self.set_tags(tags)
        self.set_ratings(ratings)
        self.set_links(links)

    def set_ratings(self, ratings):
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

    def processing_datasets(self):
        """

        @return:
        """
        pass

    def apply_filters(self):
        filters = self.config_obj['filters']

        if not filters:
            return self.ratings

        qtd_ratings = filters['qtd_ratings']
        new_ratings = self.ratings[0:qtd_ratings]
        return new_ratings

    def _get_dataset(self):
        """

        @return:
        """

        if self.proportion == "ml-25m":
            self._load_ml25m()
        if self.proportion == "ml-latest":
            self.set_mllatest()
        if self.proportion == "ml-latest-small":
            self._load_ml_latest_small()

        return [
            self.items,
            self.links,
            self.ratings,
            self.tags,
        ]

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
