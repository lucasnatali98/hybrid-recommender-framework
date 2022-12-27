from src.experiments.experiment_handler import ExperimentHandler
from lenskit.batch import recommend, predict
from joblib import dump, load
from src.tasks.task import Task
from src.data.loader import Loader
from src.utils import hrf_experiment_output_path
import pandas as pd
from src.recommenders.recommenders_container import RecommendersContainer


class AlgorithmsTask(Task):
    def __init__(self, algorithm: RecommendersContainer, args=None):
        self.experiment_output_dir = hrf_experiment_output_path()
        self.algorithm_instance: RecommendersContainer = algorithm

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
        dataset_path = self.experiment_output_dir.joinpath("preprocessing/folds/train/train-fold-1.csv")
        dataset = pd.read_csv(dataset_path)
        print("Train fold 1")
        print(dataset)

        algorithms = self._handle_algorithms_tasks(self.algorithm_instance, dataset, 'fold-1')

        return algorithms

    def _handle_algorithms_tasks(self, algorithms: RecommendersContainer, dataset: pd.DataFrame, dataset_name: str = ""):
        for algorithm in algorithms.items[0]:
            algorithm_name = algorithm.__class__.__name__
            print("Algorithm name: ", algorithm_name)
            algorithm.fit(dataset)

            path = hrf_experiment_output_path().joinpath("models/trained_models/")
            path = path.joinpath(algorithm_name + dataset_name + ".joblib")
            dump(algorithm, path)


        return None


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
