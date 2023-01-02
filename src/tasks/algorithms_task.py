from src.experiments.experiment_handler import ExperimentHandler
from joblib import dump, load
from lenskit.algorithms.ranking import TopN
from src.tasks.task import Task
from src.data.loader import Loader
from src.utils import hrf_experiment_output_path
import pandas as pd
from lenskit.algorithms import Recommender
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
        train_dataset_path = self.experiment_output_dir.joinpath("preprocessing/folds/train/train-fold-1.csv")
        test_dataset_path = self.experiment_output_dir.joinpath("preprocessing/xtest.csv")
        train_dataset = pd.read_csv(train_dataset_path, index_col=[0])
        test_dataset = pd.read_csv(test_dataset_path)


        algorithms = self._handle_algorithms_tasks(
            self.algorithm_instance,
            train_dataset,
            'fold-1',
            test_dataset
        )

        return algorithms


    def topn_process(self, algorithm, ratings: pd.DataFrame):
        print("topn process")
        user_item = ratings.drop(columns=['rating'])
        print("user_item")
        print(user_item)
        top_n = TopN(algorithm)
        preds = top_n.predict(user_item, ratings)
        return preds


    def _handle_algorithms_tasks(self,
                                 algorithms: RecommendersContainer,
                                 dataset: pd.DataFrame,
                                 dataset_name: str,
                                 test_dataset: pd.DataFrame):

        recs = None

        for algorithm in algorithms.items[0]:
            algorithm_name = algorithm.__class__.__name__
            print("Algorithm name: ", algorithm_name)
            print("Algorithm: ")
            print(algorithm)
            print(dataset.head())

            algorithm.fit(dataset)

            path = hrf_experiment_output_path().joinpath("models/trained_models/")
            path = path.joinpath(algorithm_name + dataset_name + ".joblib")
            dump(algorithm, path)

            preds = self.topn_process(algorithm, dataset)
            print("predictions: ", preds)


            recs['Algorithm'] = algorithm_name

        return recs


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


if __name__ == "__main__":
    run_algorithms_task()
