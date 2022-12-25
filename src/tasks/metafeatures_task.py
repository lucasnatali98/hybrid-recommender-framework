
from src.tasks.task import Task
from src.experiments.experiment_handler import ExperimentHandler
from src.data.loader import Loader
class MetaFeaturesTask(Task):
    def __init__(self, metafeatures, args = None):
        self.metafeatures_instance = metafeatures

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
        return metafeatures


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

    metafeatures_instance = experiment_instances['datasets']

    metafeatures_task = MetaFeaturesTask(metafeatures_instance)
    metafeatures_task.run()
    print(" => Finalizando tarefa de cálculo das metafeatures")


run_metafeatures_task()