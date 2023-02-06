from src.data.loader import Loader
from src.tasks.task import Task
from src.experiments.experiment_handler import ExperimentHandler
from src.utils import hrf_experiment_output_path

class ResultsTask(Task):
    def __init__(self, results,  args=None):
        """

        @param args:
        """
        self.results = results
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
        pass

    def _handle_results_tasks(self, results):
        """

        @param results:
        @return:
        """
        return results


def run_results_task():
    loader = Loader()
    config_obj = loader.load_json_file("config.json")
    experiments = config_obj['experiments']
    exp_handler = ExperimentHandler(
        experiments=experiments
    )

    experiment = exp_handler.get_experiment("exp1")
    experiment_instances = experiment.instances
    results_instance = experiment_instances['results']
    result_task = ResultsTask(results_instance)
    print(" => Iniciando tarefas de cálculos dos resultados")
    results = result_task.run()
    print(" => Finalizando tarefa de cálculo dos resultados")
    print("\n")
    return results

if __name__ == "__main__":
    run_results_task()
