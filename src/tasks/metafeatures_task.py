import subprocess
from src.utils import hrf_external_path
from src.tasks.task import Task
from src.experiments.experiment_handler import ExperimentHandler
from src.data.loader import Loader


class MetaFeaturesTask(Task):
    def __init__(self, metafeatures=None, args=None):
        self.metafeatures_instance = metafeatures
        self.metrics_calculator_path = hrf_external_path().joinpath("metric_calculator/")
        self.metrics_calculator_jar_path = self.metrics_calculator_path.joinpath(
            "MetricsCalculator.jar"
        )
        self.metrics_calculator_config_file_path = self.metrics_calculator_path.joinpath(
            "metric_calculator_example.xml"
        )

    def create_command_to_metrics_calculator(self):
        command = "java -jar {} {}".format(
            self.metrics_calculator_jar_path,
            self.metrics_calculator_config_file_path
        )
        print(command)
        return command

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
        metafeatures = self._handle_metafeatures_tasks(self.metafeatures_instance)
        return metafeatures

    def _handle_metafeatures_tasks(self, metafeatures):
        command = self.create_command_to_metrics_calculator()
        output = subprocess.call(
            [command],
            shell=True
        )

        return output


def run_metafeatures_task():
    print(" => Iniciando tarefa de cálculo das metafeatures")
    loader = Loader()
    config_obj = loader.load_json_file("config.json")

    experiments = config_obj['experiments']
    exp_handler = ExperimentHandler(
        experiments=experiments
    )
    experiment = exp_handler.get_experiment("exp1")
    experiment_instances = experiment.instances

    metafeatures_instance = experiment_instances['metafeatures']

    metafeatures_task = MetaFeaturesTask(metafeatures_instance)
    metafeatures_task.run()
    print(" => Finalizando tarefa de cálculo das metafeatures")
    print("\n")


if __name__ == "__main__":
    run_metafeatures_task()
