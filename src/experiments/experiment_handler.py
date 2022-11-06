from src.experiments.experiment import AbstractExperiment, Experiment
from src.shared.container import Container
from typing import List

class ExperimentHandler(Container):
    def __init__(self, experiments) -> None:
        """

        """
        super().__init__()

        experiment = Experiment(experiments[0])
        self.items.append(experiment)
    def run_experiments(self) -> dict:
        result = {}
        print("Quantidade de experimentos que serão executados: ", len(self.items))
        for experiment in self.items:
            result[experiment.experiment_id] = experiment.run()

        return result