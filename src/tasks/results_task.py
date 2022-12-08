import sys
import subprocess

from src.tasks.task import Task
from src.experiments.experiment_handler import ExperimentHandler
class ResultsTask(Task):
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

    def _handle_results_tasks(self, results):
        """

        @param results:
        @return:
        """
        return results



def main():
    exp_handler = ExperimentHandler()
    experiment = exp_handler.create_experiment_instance()
    results = experiment.results

    results_task = ResultsTask(results)
    results_task.run()
