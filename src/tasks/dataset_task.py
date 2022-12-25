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


def run_dataset_task():
    loader = Loader()
    config_obj = loader.load_json_file("config.json")

    experiments = config_obj['experiments']
    exp_handler = ExperimentHandler(
        experiments=experiments
    )
    experiment = exp_handler.get_experiment("exp1")
    print("Experiment typeof: ", experiment)
    experiment_instances = experiment.instances
    print("Experiment_instances: ", experiment_instances)
    #Não preciso criar instancias, porque elas já existem como um atributo da classe

    dataset_instance = experiment_instances['datasets']


    dataset_task = DatasetTask(dataset_instance)
    ratings = dataset_instance.ratings

    print(" => Iniciando a execução da tarefa dos datasets")
    dataset_result = dataset_task.run()
    print(" => Finalizando a tarefa dos datasets")
    dataset_result.to_csv()
    return dataset_result


run_dataset_task()






