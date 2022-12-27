from src.visualization.visualization import StaticPlot
from src.utils import process_parameters

class StaticBar(StaticPlot):
    def __init__(self, parameters: dict) -> None:
        """
        
        """
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)
        #Tipos de visualização que serão feitas
        self.plot_types = parameters['plot_types']

        self.ratings_by_user = self.plot_types['ratings_by_user']
        self.ratings_by_movie = self.plot_types['ratings_by_movie']
        self.movie_ratings_distribution = self.plot_types['movie_ratings_distribution']


    def plot(self):
        """

        @return:
        """
        pass