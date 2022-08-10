from src.data.dataset import AbstractDataSet
import os.path
from dataclasses import dataclass

PROPORTION_POSSIBILITIES = {
    "ml-25m",
    "ml-latest",
    "ml-latest-small",
}

@dataclass
class MovieLens(AbstractDataSet):
    """

    """

    def __init__(self, proportion):
        """
        @param proportion = qual a proporção do MovieLens vamos carregar

        Exemplo: ["ML100K", "MOVIELENS", "ML1M", "ML10M"]

        """
        super().__init__()
        proportion = str(proportion)

        print("Load MovieLens Proportion: ", proportion)

        if not self._is_proportion_valid(proportion):
            raise Exception(
                "A proporção da base de dados está invalida, escolha por: [ ml-25m, ml-latest, ml-latest-small]"
            )

        self.proportion = proportion
        self.basePath = "data_storage/"
        self.dataset = self._get_dataset()
        self.genomeScores = None
        self.genomeTags = None


    def _is_proportion_valid(self, proportion):
        """
        Check if the proportion is valid

        @proportion: str

        """
        if proportion in PROPORTION_POSSIBILITIES:
            return True

        return False



    def _load_ml25m(self):
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

    def _load_ml_latest(self):
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

    def _load_ml_latest_small(self):
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

    def _get_dataset(self):

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

    def ratings(self):
        return getattr(MovieLens, 'ratings')

    @property
    def tags(self):
        """

        """

        return self.tags

    @property
    def links(self):
        """

        """
        return self.links

