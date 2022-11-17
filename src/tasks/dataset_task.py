import sys
import subprocess

from src.tasks.task import Task

class DatasetTask(Task):

    def __init__(self, args = None):
        pass

    def check_args(self, args):
        """

        @param args:
        @return:
        """


    def run(self):
        """

        @return:
        """
        pass


    def _handle_with_dataset(self, dataset):
        dataset = dataset.apply_filters()
        return dataset


