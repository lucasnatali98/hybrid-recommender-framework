from src.experiments.experiment_handler import ExperimentHandler

from src.tasks.task import Task
from src.data.loader import Loader
class AlgorithmsTask(Task):
    def __init__(self, algorithm, args = None):
        """
        
        @param args:
        """
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
        algorithms = self._handle_algorithms_tasks(self.algorithm_instance)
        return algorithms

    def _handle_algorithms_tasks(self, algorithms):
        return algorithms



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