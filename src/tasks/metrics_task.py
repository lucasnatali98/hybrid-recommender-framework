import sys
import subprocess

from src.tasks.task import Task
from src.experiments.experiment_handler import ExperimentHandler

class MetricsTask(Task):
    def __init__(self, args):
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

    def _handle_metrics_tasks(self, metrics):
        pass



def main():
    #Executa todas as métricas e salva os resultados
    exp_handler = ExperimentHandler()
    experiment = exp_handler.create_experiment_instance()
    metrics = experiment.metrics
    metrics_task = MetricsTask(metrics)

    metrics_task.run()


print(" => Iniciando tarefa de cálculo das métricas")
metrics = main()
print(" => Finalizando tarefa de cálculo das métricas")

