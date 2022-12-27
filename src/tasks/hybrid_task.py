import sys
import subprocess
from src.tasks.task import Task
from src.experiments.experiment_handler import ExperimentHandler
from src.data.loader import Loader
from src.utils import hrf_experiment_output_path
class HybridTask(Task):
    def __init__(self, hybrid, args = None):
        """

        @param args:
        """
        self.hybrid_instance = hybrid
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
        hybrid = self._handle_hybrid_operations(self.hybrid_instance)
        return hybrid

    def _handle_hybrid_operations(self, hybrid):
        return hybrid

def run_hybrid_task():
    print(" => Iniciando tarefa de hibridização")
    loader = Loader()
    config_obj = loader.load_json_file("config.json")

    experiments = config_obj['experiments']
    exp_handler = ExperimentHandler(
        experiments=experiments
    )
    experiment = exp_handler.get_experiment("exp1")
    experiment_instances = experiment.instances

    hybrid_instance = experiment_instances['hybrid']

    hybrid_task = HybridTask(hybrid_instance)
    hybrid_task.run()
    print(" => Finalizando tarefa de hibridização")

run_hybrid_task()