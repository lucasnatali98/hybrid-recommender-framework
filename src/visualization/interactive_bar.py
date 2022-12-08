
from src.visualization.visualization import InteractivePlot


class InteractiveBar(InteractivePlot):
    def __init__(self, parameters: dict) -> None:
        """
        
        """
        parameters = self.process_parameters(parameters)
        self.plot_types = parameters['plot_types']
        self.ratings_by_user = self.plot_types['ratings_by_user']
        self.ratings_by_movie = self.plot_types['ratings_by_movie']
        self.items_predict = self.plot_types['items_predict']

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters:
        @return:
        """
        default_keys = [

        ]
        parameters_keys = parameters.keys()

        for key in default_keys:
            if key not in parameters_keys:
                raise KeyError("A chave obrigatória {} não foi informada no arquivo de configuração".format(key))

        return parameters

    def plot(self):
        """

        @return:
        """
        pass
