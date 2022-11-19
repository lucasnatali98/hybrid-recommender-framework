import sys
import subprocess
from src.data.loader import Loader
from src.tasks.task import Task
from src.experiments.experiment import Experiment

class DatasetTask(Task):

    def __init__(self, args = None):

        self.dataset_instance = experiment.datasets


    def check_args(self, args):
        """

        @param args:
        @return:
        """


    def run(self):
        """

        @return:
        """
        loader = Loader()
        dataset = loader.load_csv_file("data_storage/temp_files/ratings.csv")
        dataset = self._handle_with_dataset(dataset)
        return dataset



    def _handle_with_dataset(self, dataset):
        dataset = dataset.apply_filters()
        return dataset

