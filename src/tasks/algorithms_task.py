from lenskit.algorithms.basic import UnratedItemCandidateSelector
import numpy as np
from lenskit import batch
from src.experiments.experiment_handler import ExperimentHandler
from joblib import dump, load
from lenskit.algorithms.ranking import TopN
from src.tasks.task import Task
from src.data.loader import Loader
from src.utils import hrf_experiment_output_path
import pandas as pd
from lenskit.batch import predict, recommend
from lenskit.algorithms import Recommender
from src.recommenders.recommenders_container import RecommendersContainer


class AlgorithmsTask(Task):
    def __init__(self, algorithm: RecommendersContainer, args=None):
        self.algorithm_instance: RecommendersContainer = algorithm

        self.experiment_output_dir = hrf_experiment_output_path()

        self.algorithms_output_dir = self.experiment_output_dir.joinpath("models/results/")
        self.predictions_output_dir = self.algorithms_output_dir.joinpath("predictions/")
        self.rankings_output_dir = self.algorithms_output_dir.joinpath("rankings/")
        self.recommendations_output_dir = self.algorithms_output_dir.joinpath("recommendations/")

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

        algorithms = self.handle_algorithms_tasks(
            self.algorithm_instance,
            train_dataset[0:2000],
            'fold-1',
            test_dataset
        )

        return algorithms

    def topn_process(self, algorithm, ratings: pd.DataFrame):
        users = np.unique(ratings['user'].values)
        items = ratings['item'].values

        algorithm.fit(ratings)
        select = UnratedItemCandidateSelector()

        topn_dataframe = pd.DataFrame(columns=['user', 'item', 'score'])

        top_n = TopN(algorithm, select)
        number_of_items_rankeds = 10
        for u in users:
            recs = top_n.recommend(
                u,
                number_of_items_rankeds,
                items
            )

            user_id = [u] * number_of_items_rankeds
            algorithm_name = [algorithm.__class__.__name__] * number_of_items_rankeds
            recs['user'] = pd.Series(user_id)
            recs['algorithm'] = pd.Series(algorithm_name)
            topn_dataframe = pd.concat([topn_dataframe, recs], ignore_index=True)

        topn_dataframe.to_csv(self.algorithms_output_dir.joinpath("ranking.csv"), index=False)
        return topn_dataframe
    def handle_algorithms_tasks(self,
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

            self.topn_process(algorithm, dataset)
            dataset_copy = dataset.copy()
            dataset_copy.drop(columns=['rating'], inplace=True)

            preds = predict(algorithm, dataset)
            preds.to_csv(self.predictions_output_dir.joinpath("predictions.csv"), index=False)
            print(preds)
            users = np.unique(test_dataset['user'].values)

            recs = algorithm.recommend(users, 10)
            recs.to_csv(self.recommendations_output_dir.joinpath("recommendations.csv"), index=False)


            print("recs - task: ", recs)

        return preds


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
