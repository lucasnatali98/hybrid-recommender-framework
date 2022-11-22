import sys
import subprocess
from src.data.loader import Loader
from src.tasks.task import Task

from src.experiments.experiment import Experiment


class DatasetTask(Task):

    def __init__(self, dataset):
        self.dataset_instance = dataset

    def check_args(self, args):
        """

        @param args:
        @return:
        """
        pass

    def run(self, dataset=None):
        """

        @return:
        """
        # loader = Loader()
        # dataset = loader.load_csv_file("data_storage/temp_files/ratings.csv")
        dataset = self._handle_with_dataset(self.dataset_instance)
        return dataset

    def _handle_with_dataset(self, dataset):
        dataset = dataset.apply_filters()
        return dataset


def main():
    loader = Loader()

    config_obj = loader.load_json_file("config.json")
    experiments = config_obj['experiments']
    cluster_info = config_obj['cluster_info']
    recipes_default = config_obj['recipesDefault']
    experiment_dependencies = config_obj['experiment_dependencies']
    experiment = Experiment(
        experiment_obj=experiments[0],
        recipes_default=recipes_default,
        experiment_dependencies=experiment_dependencies
    )

    dataset_instance = experiment.datasets

    dataset_task = DatasetTask(dataset_instance)

    ratings = dataset_instance.ratings

    dataset_result = dataset_task.run()
    return dataset_result

main()
