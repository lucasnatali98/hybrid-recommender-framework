from src.experiments.experiment_handler import ExperimentHandler
import pickle
from src.tasks.task import Task
from src.data.loader import Loader
from src.utils import hrf_experiment_output_path
import pandas as pd


class AlgorithmsTask(Task):
    def __init__(self, algorithm, args=None):
        self.experiment_output_dir = hrf_experiment_output_path()
        self.algorithm_instance = algorithm

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
        dataset = pd.read_csv()
        algorithms = self._handle_algorithms_tasks(self.algorithm_instance, dataset)
        return algorithms

    def _handle_algorithms_tasks(self, algorithms, dataset):
        for algorithm in algorithms:
            # Percorrer todas
            algorithm.fit()
            algorithm_name = algorithm.__class__.__name__
            print("Algorithm name: ", algorithm_name)
            path = hrf_experiment_output_path().joinpath("models/trained_models/")
            pickle.dump(algorithm, path)


def run_algorithms_task():
    print(" => Inicio da tarefa dos algoritmos")
    loader = Loader()
    config_obj = loader.load_json_file("config.json")

    experiments = config_obj['experiments']
    exp_handler = ExperimentHandler(
        experiments=experiments
    )
    experiment = exp_handler.get_experiment("exp1")
    experiment_instances = experiment.instances

    algorithms = experiment_instances['recommenders']
    algorithms_task = AlgorithmsTask(algorithms)
    algorithms_task.run()

    print(" => Finalizando a tarefa dos algoritmos")


run_algorithms_task()
