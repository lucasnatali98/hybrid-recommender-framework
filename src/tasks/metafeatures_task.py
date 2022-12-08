import sys
import subprocess

from src.tasks.task import Task
from src.experiments.experiment_handler import ExperimentHandler
class MetaFeaturesTask(Task):
    def __init__(self, args = None):
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


    def _handle_metafeatures_tasks(self, metafeatures):
        return metafeatures


def main():
    exp_handler = ExperimentHandler()
    experiment = exp_handler.create_experiment_instance()
    metafeatures = experiment.metafeatures
    metafeatures_task = MetaFeaturesTask(metafeatures)
    metafeatures_task.run()