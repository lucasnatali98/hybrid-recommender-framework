from src.data.loader import Loader
from src.experiments.experiment_handler import ExperimentHandler
from src.tasks.metrics_task import MetricsTask
from src.utils import hrf_experiment_output_path

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



class TestMetricsTask:
    def test_topn_evaluate(self):

        metrics_task.topn_evaluation(
            metrics=[
                "ndcg",
                "hit",
                "precision",
                "recall"
            ]
        )

