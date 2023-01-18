from src.visualization.visualization import InteractivePlot
from src.utils import process_parameters


class InteractiveBar(InteractivePlot):
    def __init__(self, parameters: dict) -> None:
        """
        
        """
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)
        self.plot_types = parameters.get('plot_types')
        self.ratings_by_user = self.plot_types.get('ratings_by_user')
        self.ratings_by_movie = self.plot_types.get('ratings_by_movie')
        self.items_predict = self.plot_types.get('items_predict')

    def plot(self):
        """

        @return:
        """
        pass
