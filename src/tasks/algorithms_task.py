import sys
import subprocess
from src.experiments.experiment_handler import ExperimentHandler
from src.tasks.task import Task

class AlgorithmsTask(Task):
    def __init__(self, args = None):
        """
        
        @param args:
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

    def _handle_algorithms_tasks(self, algorithms):
        return algorithms



def main():
    exp_handler = ExperimentHandler()
    experiment = exp_handler.create_experiment_instance()
    algorithms = experiment.recommenders
    algorithms_task = AlgorithmsTask(algorithms)
    algorithms_task.run()


print(" => Inicio da tarefa dos algoritmos")
algorithms_result = main()
print(" => Finalizando a tarefa dos algoritmos")