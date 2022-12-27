from src.tasks.task import Task
from src.experiments.experiment_handler import ExperimentHandler
from src.data.loader import Loader
from src.utils import hrf_experiment_output_path
class MetricsTask(Task):
    def __init__(self, metrics, args = None):
        """

        @param args:
        """
        self.metric_instances = metrics
        self.experiment_output_dir = hrf_experiment_output_path()

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