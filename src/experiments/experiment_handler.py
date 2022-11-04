from src.experiments.experiment import AbstractExperiment
from src.shared.container import Container
class ExperimentHandler(Container):

    def __init__(self, experiments) -> None:
        """

        """
        super().__init__()
        self.insert(0, experiments)
