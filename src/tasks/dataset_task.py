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
    """
    Não posso passar chumbado qual o experimento é... ou eu descubro pelo arquivo de configuração
    buscando pelo nome ou algo assim ou eu recebo como argumentos para executar o programa, essa opção
    é menos viável visto que dependente de uma alteração no Xperimentor
    """
    experiment = exp_handler.get_experiment("exp1")
    experiment_instances = experiment.instances

    dataset_instance = experiment_instances['datasets']

    dataset_task = DatasetTask(dataset_instance)

    print(" => Iniciando a execução da tarefa dos datasets")
    dataset_result = dataset_task.run()
    print("Dataset resultante: ", dataset_result)
    print(" => Finalizando a tarefa dos datasets")

    load_dataset = dataset_result.to_csv()

    if load_dataset is None:
        print("Ocorreu um problema na hora de salvar o dataset resultante")
        return

    return dataset_result


run_dataset_task()






