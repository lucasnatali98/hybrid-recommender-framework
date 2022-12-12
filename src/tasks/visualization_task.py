from src.tasks.task import Task
from src.experiments.experiment_handler import ExperimentHandler

class VisualizationTask(Task):
    def __init__(self, args):
        """

        """
        pass

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
        pass

    def _handle_visualization_task(self, visualization):
        """

        @param results:
        @return:
        """
        return visualization

def main():
    exp_handler = ExperimentHandler()
    experiment = exp_handler.create_experiment_instance()
    visualization = experiment.visualization
    visualization_task = VisualizationTask(visualization)
    visualization_task.run()

print(" => Inicio da tarefa de visualização dos dados")
visualization = main()
print(" => Finalizando tarefa de visualização dos dados")

