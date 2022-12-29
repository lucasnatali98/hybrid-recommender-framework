import pandas as pd
from src.data.movielens import MovieLens
import matplotlib.pyplot as plt
from src.visualization.visualization import StaticPlot
from src.utils import process_parameters, hrf_experiment_output_path


class StaticScatter(StaticPlot):
    def __init__(self, parameters: dict) -> None:

        default_keys = set()
        parameters = process_parameters(parameters, default_keys)


        self.visualization_output_path = "visualization/static/scatter/"
        self.plot_types = parameters['plot_types']

        self.ratings_by_user = self.plot_types['ratings_by_user']
        self.ratings_by_movie = self.plot_types['ratings_by_movie']
        self.movie_ratings_distribution = self.plot_types['movie_ratings_distribution']




    def plot(self):
        """

        @return:
        """
        ratings = MovieLens({
            'proportion': 'ml-latest-small',
            'filters': {}
        }).ratings

        self.ratings_by_user_plot(ratings)
        self.ratings_by_movie_plot(ratings)


    def ratings_by_user_plot(self, ratings: pd.DataFrame):
        print("ratings by user scatter plot")
        df = ratings.groupby(by=['user'], axis=0).count()
        df = df.reset_index()
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.scatter(df['user'], df['rating'])
        ax.set_title("Quantidade de Ratings por usuário")
        ax.set_ylabel("Quantidade de ratings")
        ax.set_xlabel("Id dos usuários")
        archive_name = "ratings_by_user.png"
        path_to_save = hrf_experiment_output_path().joinpath(self.visualization_output_path).joinpath(archive_name)
        fig.savefig(path_to_save)
        return df


    def ratings_by_movie_plot(self, ratings: pd.DataFrame):
        print("ratings by movie scatter plot")
        df = ratings.groupby(by=['item'], axis=0).count()
        df = df.reset_index()
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.scatter(df['user'], df['rating'])
        ax.set_title("Quantidade de Ratings por filme")
        ax.set_ylabel("Quantidade de ratings")
        ax.set_xlabel("Id dos filmes")
        archive_name = "ratings_by_movie.png"
        path_to_save = hrf_experiment_output_path().joinpath(self.visualization_output_path).joinpath(archive_name)
        fig.savefig(path_to_save)
        return df
