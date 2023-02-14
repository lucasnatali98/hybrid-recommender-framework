from lenskit.algorithms.basic import UnratedItemCandidateSelector
import numpy as np
from src.experiments.experiment_handler import ExperimentHandler
from joblib import dump, load
from src.tasks.task import Task
from src.data.loader import Loader
from src.utils import hrf_experiment_output_path, check_if_directory_exists, create_directory
import pandas as pd
from src.recommenders.recommenders_container import RecommendersContainer
import os
import traceback
from src.recommenders.batch import LenskitBatch


class AlgorithmsTask(Task):
    def __init__(self, algorithm: RecommendersContainer, args=None):
        self.algorithm_instances: RecommendersContainer = algorithm
        self.number_of_recommendations = self.algorithm_instances.number_of_recommendations
        self.experiment_output_dir = hrf_experiment_output_path()
        self.preprocessing_output_dir = self.experiment_output_dir.joinpath("preprocessing/")
        self.algorithms_output_dir = self.experiment_output_dir.joinpath("models/results/")
        self.predictions_output_dir = self.algorithms_output_dir.joinpath("predictions/")
        self.rankings_output_dir = self.algorithms_output_dir.joinpath("rankings/")
        self.recommendations_output_dir = self.algorithms_output_dir.joinpath("recommendations/")
        self.lenskit_batch = LenskitBatch()

    def check_args(self, args):
        pass

    def get_fold_file_names(self, fold_type: str) -> list:
        if fold_type not in ['train', 'validation']:
            raise Exception("O valor de fold_type está invalido, tente: train ou validation")

        folds_directory = self.preprocessing_output_dir.joinpath("folds/{}/".format(fold_type))
        file_names = []
        for path in os.scandir(folds_directory):
            if path.is_file():
                file_names.append(path.name)

        return file_names

    def get_default_files_to_train_and_test(self):
        default_splitted_files = {
            "xtrain": self.preprocessing_output_dir.joinpath('xtrain.csv'),
            "xtest": self.preprocessing_output_dir.joinpath('xtest.csv'),
            "ytest": self.preprocessing_output_dir.joinpath('ytest.csv'),
            "ytrain": self.preprocessing_output_dir.joinpath('ytrain.csv')
        }
        return default_splitted_files

    def check_if_folds_is_empty(self) -> bool:
        """
        Função para verificar se os folds existem, com o objetivo de decidir se eles serõo usados
        ou se a aplicação vai utilizar os dados a partir de sua divisão normal.

        @return: bool
        """

        folds_path = self.preprocessing_output_dir.joinpath(
            "folds/train/"
        )

        folds_dir = os.listdir(folds_path)
        if len(folds_dir) == 0:
            return False

        return True

    def fold_execution(self):
        train_fold_files = self.get_fold_file_names('train')
        validation_fold_files = self.get_fold_file_names('validation')
        fold_files = zip(train_fold_files, validation_fold_files)

        if len(train_fold_files) == 0:
            raise Exception("Os arquivos de fold de treino não foram encontrados")

        test_dataset_path = self.experiment_output_dir.joinpath("preprocessing/xtest.csv")
        test_dataset = pd.read_csv(test_dataset_path)

        content_based_df_path = self.experiment_output_dir.joinpath("preprocessing/content-based-dataset.csv")
        content_based_df = pd.read_csv(content_based_df_path)

        for train_file, validation_file in fold_files:
            train_dataset_path = self.preprocessing_output_dir.joinpath("folds/train/").joinpath(train_file)
            validation_dataset_path = self.preprocessing_output_dir.joinpath("folds/validation").joinpath(
                validation_file)

            train_dataset = pd.read_csv(train_dataset_path, index_col=[0])
            validation_dataset = pd.read_csv(validation_dataset_path, index_col=[0])

            fold_name = train_file.split(".")
            fold_name = fold_name[0]

            self.handle_algorithms_tasks(
                self.algorithm_instances,
                train_dataset,
                fold_name,
                validation_dataset,
                content_based_df
            )

        return True

    def default_execution(self):
        files_path = self.get_default_files_to_train_and_test()
        try:
            xtrain = pd.read_csv(files_path.get('xtrain'))
            ytrain = pd.read_csv(files_path.get('ytrain'))
            ytest = pd.read_csv(files_path.get('ytest'))
            xtest = pd.read_csv(files_path.get('xtest'))

            algorithms = self.handle_algorithms_task_default(
                algorithms=self.algorithm_instances,
                xtrain=xtrain,
                xtest=xtest,
                ytrain=ytrain,
                ytest=ytest,
                train_dataset_name='xtrain'
            )

            return algorithms
        except Exception as e:
            print(e)

    def run(self):
        try:
            is_folds_directory_exists = self.check_if_folds_is_empty()
            if is_folds_directory_exists is True:
                result = self.fold_execution()
                return result
            else:
                result = self.default_execution()
                return result

        except Exception as e:
            print(e)
            print(traceback.print_exc())

    def _recommend_to_content_based(self, algorithm, algorithm_name, dataset, dataset_name):
        algorithm.fit(dataset)
        recs = algorithm.recommend(None, 0, dataset)
        if recs is not None:
            recommendation_file_name = algorithm_name + "-" + dataset_name + "-" + "recommendations-content-based.csv"
            recs.to_csv(self.recommendations_output_dir.joinpath(recommendation_file_name), index=False)

    def handle_algorithms_task_default(self,
                                       algorithms: RecommendersContainer,
                                       xtrain: pd.DataFrame = pd.DataFrame(),
                                       xtest: pd.DataFrame = pd.DataFrame(),
                                       ytrain: pd.Series = None,
                                       ytest: pd.Series = None,
                                       content_based_dataset: pd.DataFrame = pd.DataFrame(),
                                       train_dataset_name: str = ""
                                       ):

        try:
            for algorithm in algorithms.items[0]:
                algorithm_name = algorithm.__class__.__name__
                print("Algorithm name: ", algorithm_name)
                print("dataset_name:", train_dataset_name)

                if algorithm_name == "ContentBasedRecommender":
                    self._recommend_to_content_based(
                        algorithm, algorithm_name, content_based_dataset, "movies"
                    )
                    continue

                algorithm.fit(xtrain)

                self.save_trained_model(algorithm, algorithm_name, train_dataset_name)

                preds = self.lenskit_batch.predict(algorithm, xtrain[['user', 'item']])
                if preds is not None:
                    self.save_results(
                        'predictions',
                        preds,
                        algorithm_name,
                        train_dataset_name,
                        'csv'
                    )
                users = np.unique(xtest['user'].values)

                recs = self.lenskit_batch.recommend(
                    algorithm.recommender,
                    users,
                    self.number_of_recommendations
                )
                if recs is not None:
                    self.save_results(
                        'recommendations',
                        recs,
                        algorithm_name,
                        train_dataset_name,
                        'csv'
                    )

            return True

        except Exception as err:
            print("Error: ", err)
            print(traceback.print_exc())
            return None

    def save_results(self, result_type: str, result, algorithm_name: str, dataset_name: str, extension: str):
        possible_result_types = ['predictions', 'recommendations']
        if result_type not in possible_result_types:
            raise Exception(
                "Não foi possível realizar o armazenamento do resultado de tipo {}".format(result_type)
            )

        dirs = {
            'predictions': self.predictions_output_dir,
            'recommendations': self.recommendations_output_dir,
            'ranking': self.rankings_output_dir
        }

        dir_to_save = dirs.get(result_type, None)
        if dir_to_save is None:
            raise Exception(
                "Não foi possivel obter o diretório para salvar os resultados"
            )

        file_name = "{}-{}-predictions.{}".format(algorithm_name, dataset_name, extension)
        result.to_csv(dir_to_save.joinpath(file_name), index=False)

    def save_trained_model(self, algorithm, algorithm_name: str, dataset_name: str):
        path = hrf_experiment_output_path().joinpath("models/trained_models/")
        path = path.joinpath(algorithm_name + "-" + dataset_name + ".joblib")
        dump(algorithm, path)

    def handle_algorithms_tasks(self,
                                algorithms: RecommendersContainer,
                                dataset: pd.DataFrame,
                                dataset_name: str,
                                test_dataset: pd.DataFrame,
                                content_based_dataset: pd.DataFrame):

        try:
            for algorithm in algorithms.items[0]:
                algorithm_name = algorithm.__class__.__name__
                print("Algorithm name: ", algorithm_name)
                print("dataset_name:", dataset_name)

                if algorithm_name == "ContentBasedRecommender":
                    self._recommend_to_content_based(
                        algorithm, algorithm_name, content_based_dataset, "movies"
                    )
                    continue

                algorithm.fit(dataset)

                self.save_trained_model(algorithm, algorithm_name, dataset_name)

                preds = self.lenskit_batch.predict(algorithm, dataset[['user', 'item']])
                if preds is not None:
                    self.save_results(
                        'predictions',
                        preds,
                        algorithm_name,
                        dataset_name,
                        'csv'
                    )

                users = np.unique(test_dataset['user'].values)

                recs = self.lenskit_batch.recommend(
                    algorithm.recommender,
                    users,
                    self.number_of_recommendations,
                )
                if recs is not None:
                    self.save_results(
                        'recommendations',
                        recs,
                        algorithm_name,
                        dataset_name,
                        'csv'
                    )

            return True

        except Exception as err:
            print("Error: ", err)
            print(traceback.print_exc())
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
    print("\n")


if __name__ == "__main__":
    run_algorithms_task()
