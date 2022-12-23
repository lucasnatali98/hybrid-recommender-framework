from src.experiments.experiment import AbstractExperiment, Experiment
from src.shared.container import Container
from typing import List
from external.deploy import Xperimentor, TaskExecutor
from src.experiments.experiment_tasks import ExperimentTask

class ExperimentHandler(Container):
    def __init__(self, experiments: list = None) -> None:
        super().__init__()
        self._experiments = []
        self._experiment_tasks = ExperimentTask().define_all_tasks()

        if experiments is None:
            pass
        else:
            #Chamar build experiments
            self.build_experiments(experiments=experiments)



    def build_experiments(self, experiments: list):
        """
        Responsável por construir as instancias e o arquivo de configuração do Xperimentor
        @param experiments:
        @param experiment_dependencies:
        @param recipes_default:
        @param cluster_info:
        @return:
        """

        for experiment in experiments:
            self.create_experiment_instance(experiment)

    def run_experiments(self) -> dict:
        result = {}
        for experiment in self.items:
            print("run experiment: ", experiment.run())
            #result[experiment._experiment_id] = experiment.run()

        return result

    def create_experiment_instance(self, experiment: dict):
        """
        Essa função cria uma instancia de um experimento a partir dos arquivos de configuração,
        uma instancia de um experimento envolve todas as classes presentes no experimento, ou seja,
        teremos instancia de um dataset, de diferentes pre-processamentos, algoritmos, dentre outros.

        @return: Experiment
        """

        experiment = Experiment(
            experiment = experiment
        )

        self._experiments.append(experiment)
