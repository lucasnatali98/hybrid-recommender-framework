from src.tasks.task import Task
from src.experiments.experiment_handler import ExperimentHandler
from src.data.loader import Loader

class VisualizationTask(Task):
    def __init__(self, visualization):
        """

        """

        self.visualization_instance = visualization

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters:
        @return:
        """
        pass

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
        visualizations = self._handle_visualization_task(self.visualization_instance)
        return visualizations
    def _handle_visualization_task(self, visualization):
        """

        @param results:
        @return:
        """
        return visualization


def run_visualization_task():
    loader = Loader()
    config_obj = loader.load_json_file("config.json")

    experiments = config_obj['experiments']
    exp_handler = ExperimentHandler(
        experiments=experiments
    )

    experiment = exp_handler.get_experiment("exp1")
    experiment_instances = experiment.instances

    visualization_instance = experiment_instances['datasets']

    visualization_task = VisualizationTask(visualization_instance)

    print(" => Iniciando a execução da tarefa da visualização dos dados")
    visualization_result = visualization_task.run()
    print("Dataset resultante: ", visualization_result)
    print(" => Finalizando a tarefa de visualização dos dados")

    load_dataset = dataset_result.to_csv()

    if load_dataset is None:
        print("Ocorreu um problema na hora de salvar o dataset resultante")
        return

    return dataset_result


run_visualization_task()
