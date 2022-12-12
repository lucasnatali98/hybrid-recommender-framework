import sys
import subprocess
from src.data.loader import Loader
from src.tasks.task import Task
from src.experiments.experiment import Experiment
from src.experiments.experiment_handler import ExperimentHandler
import logging


class DatasetTask(Task):
    """

    """
    def __init__(self, dataset):
        """

        @param dataset:
        """
        self.dataset_instance = dataset

    def check_args(self, args):
        pass
    def run(self):
        """
        Essa função irá realizar todos os processos definidos para o conjunto de dados
        a partir do arquivo de configuração

        @return:
        """

        dataset = self._handle_operations_dataset(self.dataset_instance)
        return dataset

    def _handle_operations_dataset(self, dataset):
        """

        @param dataset:
        @return:
        """
        dataset = dataset.apply_filters()

        return dataset


def main():

    exp_handler = ExperimentHandler()
    experiment = exp_handler.create_experiment_instance()
    dataset_instance = experiment.datasets
    dataset_task = DatasetTask(dataset_instance)
    ratings = dataset_instance.ratings
    dataset_result = dataset_task.run()
    return dataset_result



logging.info(" => Iniciando a execução da tarefa dos datasets")
new_dataset = main()
new_dataset.to_csv()
print(" => Finalizando a tarefa dos datasets")
