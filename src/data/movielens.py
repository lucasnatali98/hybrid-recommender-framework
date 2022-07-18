from src.data.dataset import AbstractDataSet
import os.path

PROPORTION_POSSIBILITIES = {
    "ml-25m",
    "ml-latest",
    "ml-latest-small",
}


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

        if not self._is_proportion_valid(proportion):
            raise Exception(
                "A proporção da base de dados está invalida, escolha por: [ ml-25m, ml-latest, ml-latest-small]"
            )

        self.proportion = proportion
        self.basePath = "data_storage/"
        self.dataset = self._get_dataset()





    def _is_proportion_valid(self, proportion):
        if proportion in PROPORTION_POSSIBILITIES:
            return True

        return False

    def _set_ml25m(self):
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

        self.movies = movies
        self.links = links
        self.ratings = ratings
        self.tags = tags
        self.genomeScores = genome_scores
        self.genomeTags = genome_tags

    def _set_ml_latest(self):
        """

        """
        path = self.basePath + "ml-25m/"
        movies = self.Loader.load_file(path=path + "movies", extension=".csv")
        links = self.Loader.load_file(path=path + "links", extension=".csv")
        ratings = self.Loader.load_file(path=path + "ratings", extension=".csv")
        tags = self.Loader.load_file(path=path + "tags", extension=".csv")
        genome_scores = self.Loader.load_file(path=path + "genome-scores", extension=".csv")
        genome_tags = self.Loader.load_file(path=path + "genome-tags", extension=".csv")

        self.movies = movies
        self.links = links
        self.ratings = ratings
        self.tags = tags
        self.genomeScores = genome_scores
        self.genomeTags = genome_tags


    def _set_ml_latest_small(self):
        """


        """
        path = self.basePath + "ml-latest-small/"
        movies = self.Loader.load_file(path=path + "movies", extension=".csv")
        links = self.Loader.load_file(path=path + "links", extension=".csv")
        ratings = self.Loader.load_file(path=path + "ratings", extension=".csv")
        tags = self.Loader.load_file(path=path + "tags", extension=".csv")

        print("movies: ", movies)
        print("links: ", links)
        print("ratings: ", ratings)
        print("tags: ", tags)

        self.movies = movies
        self.links = links
        self.ratings = ratings
        self.tags = tags

    def set_genome_tags(self, genome_tags):
        self.genomeTags = genome_tags

    def set_genome_scores(self, genome_scores):
        self.genomeScores = genome_scores


    def _get_dataset(self):

        if self.proportion == "ml-25m":
            self._set_ml25m()
        if self.proportion == "ml-latest":
            self.set_mllatest()
        if self.proportion == "ml-latest-small":
            self._set_ml_latest_small()

        return [
            self.movies,
            self.links,
            self.ratings,
            self.tags,
        ]

    def ratings(self):
        """
        
        """

        return self.ratings

    def items(self):
        """
        
        """
        return self.items

    def users(self):
        """
        
        """
        return self.users

    def tags(self):
        """

        """

        return self.tags

    def links(self):
        """

        """
        return self.links
