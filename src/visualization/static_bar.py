from src.visualization.visualization import StaticPlot


class StaticBar(StaticPlot):
    def __init__(self, parameters: dict) -> None:
        """
        
        """
        parameters = self.process_parameters(parameters)
        self.plot_types = parameters['plot_types']
        self.ratings_by_user = self.plot_types['ratings_by_user']
        self.ratings_by_movie = self.plot_types['ratings_by_movie']




    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters:
        @return:
        """
        default_keys = [
            'plot_types'
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