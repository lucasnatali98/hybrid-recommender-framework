import pandas as pd
import os
from src.tasks.task import Task
from src.experiments.experiment_handler import ExperimentHandler
from src.data.loader import Loader
from src.utils import hrf_experiment_output_path
from lenskit import topn
from lenskit.metrics.predict import user_metric, global_metric, rmse, mae
from src.metrics.cross_validation import CrossValidation


class MetricsTask(Task):
    def __init__(self, metrics, args=None):
        self.metric_instances = metrics

        self.predictions_output_path = hrf_experiment_output_path().joinpath(
            "models/results/predictions/"
        )
        self.evaluate_output_path = hrf_experiment_output_path().joinpath(
            "evaluate/"
        )
        self.experiment_output_dir = hrf_experiment_output_path()
        self.preprocessing_output_dir = self.experiment_output_dir.joinpath("preprocessing/")
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
        metrics = self.handle_metrics_tasks(self.metric_instances)
        return metrics

    def get_truth_data_file_names(self):
        """
        Vai buscar todos os arquivos de validação (folds) e usa-los para testar as
        predições

        @return:
        """
        validation_folds_dir = self.preprocessing_output_dir.joinpath("folds/validation/")
        file_names = []
        for path in os.scandir(validation_folds_dir):
            if path.is_file():
                file_names.append(path.name)

        return file_names

    def get_results_file_names(self, result_type: str) -> list:
        if result_type not in ['recommendations', 'predictions', 'rankings']:
            raise Exception("O valor de fold_type está invalido, tente: train ou validation")

        folds_directory = self.algorithms_output_dir.joinpath("{}/".format(result_type))
        file_names = []
        for path in os.scandir(folds_directory):
            if path.is_file():
                file_names.append(path.name)

        return file_names

    def evaluate_predictions(self, prediction: pd.DataFrame, truth: pd.DataFrame):
        pass

    def topn_evaluation(self,
                        metrics,
                        recommendations: pd.DataFrame,
                        dataset_test: pd.DataFrame) -> pd.DataFrame:

        topn_metrics = {
            'ndcg': topn.ndcg,
            'dcg': topn.dcg,
            'precision': topn.precision,
            'recall': topn.recall,
            'hit': topn.hit

        }

        all_recs = recommendations
        test_data = dataset_test
        metrics = ['ndcg', 'dcg', 'recall']
        topn_analysis = topn.RecListAnalysis()
        for metric in metrics:
            m = topn_metrics[metric]
            topn_analysis.add_metric(m)

        results = topn_analysis.compute(all_recs, test_data)
        return results

    def handle_with_recommendation_results(self, metrics):
        print("=> Handle with recommendation results \n")
        rec_files = self.get_results_file_names('recommendations')
        truth_files = self.get_truth_data_file_names()

        for file in rec_files:
            rec_path = self.recommendations_output_dir.joinpath(file)
            recommendation = pd.read_csv(rec_path)
            file_name_elements = file.split("-")
            if file_name_elements[0] == "ContentBasedRecommender":
                continue

            fold_number = file.split("-")[3]
            truth_path = self.preprocessing_output_dir.joinpath("folds/validation/")
            truth_path = truth_path.joinpath("validation-fold-{}.csv".format(fold_number))
            truth_df = pd.read_csv(truth_path, index_col=[0])
            print("truth df: ", truth_df)

            topn_result = self.topn_evaluation(
                metrics,
                recommendation,
                truth_df
            )

            topn_result.to_csv(self.evaluate_output_path.joinpath("TopN-{}".format(file)))

    def handle_with_prediction_results(self):
        pred_files = self.get_results_file_names('predictions')
        truth_files = self.get_truth_data_file_names()
        for file in pred_files:
            print("prediction path: ", file)

            fold_number = file.split("-")[3]
            pred_path = self.predictions_output_path.joinpath(file)
            prediction = pd.read_csv(pred_path)
            truth_path = self.preprocessing_output_dir.joinpath("folds/validation/")
            truth_path = truth_path.joinpath("validation-fold-{}.csv".format(fold_number))
            print("truth_path: ", truth_path)
            truth_df = pd.read_csv(truth_path, index_col=[0])
            print("truth df: ", truth_df)

            self.evaluate_predictions(prediction, truth_df)

    def handle_metrics_tasks(self, metrics):
        self.handle_with_prediction_results()
        self.handle_with_recommendation_results(metrics)

def run_metrics_task():
    loader = Loader()
    config_obj = loader.load_json_file("config.json")

    experiments = config_obj['experiments']
    exp_handler = ExperimentHandler(
        experiments=experiments
    )
    experiment = exp_handler.get_experiment("exp1")
    experiment_instances = experiment.instances

    metrics_instance = experiment_instances['metrics']

    metrics_task = MetricsTask(metrics_instance)

    print(" => Iniciando tarefa de cálculo das métricas")
    print(" => Finalizando tarefa de cálculo das métricas")

    metrics_task.run()


run_metrics_task()
