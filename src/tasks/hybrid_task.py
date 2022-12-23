import sys
import subprocess
from src.tasks.task import Task
from src.experiments.experiment_handler import ExperimentHandler

class HybridTask(Task):
    def __init__(self, args = None):
        """

        @param args:
        """
        pass

    def check_args(self, args):
        """

        @param args:
        @return:
        """
        pass

    def run(self):
        """

        @return:
        """
        pass


def main():
    exp_handler = ExperimentHandler()
    experiment = exp_handler.create_experiment_instance()
    hybrid = experiment.hybrid
    hybrid_task = HybridTask(hybrid)
    hybrid_task.run()
