from src.visualization.visualization import InteractivePlot
from src.utils import process_parameters

class InteractiveScatter(InteractivePlot):
    def __init__(self, parameters: dict) -> None:
        """
        
        """
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def plot(self):
        """

        @return:
        """