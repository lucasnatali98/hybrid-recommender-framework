from src.visualization.visualization import TablePlot
from src.utils import process_parameters

class HtmlTable(TablePlot):
    def __init__(self, parameters: dict) -> None:
        """
        
        """
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)


    def plot(self):
        """

        @return:
        """
        pass
