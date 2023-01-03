import pandas as pd

from src.tasks.task import Task
from src.experiments.experiment_handler import ExperimentHandler
from src.data.loader import Loader
from src.utils import hrf_experiment_output_path
from lenskit import topn
from src.metrics.cross_validation import CrossValidation
class MetricsTask(Task):
    def __init__(self, metrics, args = None):
        """

        @param args:
        """
        self.cross_validation = CrossValidation({

        })
        self.metric_instances = metrics
        self.experiment_output_dir = hrf_experiment_output_path()
        self.predictions_output_path = hrf_experiment_output_path().joinpath(
            "models/results/predictions/"
        )
        self.evaluate_output_path = hrf_experiment_output_path().joinpath(
            "evaluate/"
        )

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
        metrics = self._handle_metrics_tasks(self.metric_instances)
        return metrics


    def topn_evaluation(self, metrics: list, recommendations: pd.DataFrame,  dataset_test: pd.DataFrame) -> pd.DataFrame:
        print("topn_evaluation")
        topn_metrics = {
            'ndcg': topn.ndcg,
            'dcg': topn.dcg,
            'precision': topn.precision,
            'recall': topn.recall,
            'hit': topn.hit
        }

        all_recs = recommendations
        test_data = dataset_test

        topn_analysis = topn.RecListAnalysis()
        for metric in metrics:
            m = topn_metrics[metric]
            topn_analysis.add_metric(m)

        results = topn_analysis.compute(all_recs, test_data)
        print("")
        return results


    def _handle_metrics_tasks(self, metrics):
        return metrics



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