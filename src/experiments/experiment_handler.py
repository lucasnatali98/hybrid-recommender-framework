from dataclasses import dataclass
from src.experiments.experiment import Experiment
from src.instance_factory import InstanceFactory
from src.experiments.experiment import AbstractExperiment

class ExperimentHandler:
    experiment: AbstractExperiment
    def __init__(self) -> None:
        """

        """
        self.experiments = []

    def run(self):
        """

        @return:
        """
        pass

   def _handle_with_dataset(self, dataset):
        pass



    def add(self, experiment) -> None:
        """

        @param experiment:
        @return:
        """
        pass

    def insert(self, experiments) -> None:
        """

        @param experiments:
        @return:
        """
        pass

    def remove(self, experiment) -> None:
        """

        @param experiment: dict
        @return:
        """
        self.experiments.remove(experiment)

    def removeAll(self) -> None:
        """

        @return:
        """
        self.experiments.clear()
