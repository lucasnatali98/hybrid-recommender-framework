import sys
import importlib

task_map = {
    "dataset": {
        "module": "src.tasks.dataset_task",
        "class_name": "DatasetTask"
    },
    "preprocessing": {
        "module": "src.tasks.preprocessing_task",
        "class_name": "PreProcessingTask"
    },
    "metafeatures": {
        "module": "src.tasks.metafeatures_task",
        "class_name": "MetaFeaturesTask"
    },
    "recommenders": {
        "module": "src.tasks.algorithms_task",
        "class_name": "AlgorithmsTask"
    },
    "metrics": {
        "module": "src.tasks.metrics_task",
        "class_name": "MetricsTask"
    },
    "results": {
        "module": "src.tasks.results_task",
        "class_name": "ResultsTask"
    },
    "visualization": {
        "module": "src.tasks.visualization_task",
        "class_name": "VisualizationTask"
    }
}


class TaskFactory:
    """
    Classe responsável pela criação de instancias de tarefas, essas tarefas são divididas assim como os módulos
    desse framework, teremos tarefas dos seguintes tipos:

    - Dataset task
    - Preprocessing task
    - Metafeatures task
    - Metrics task
    - Visualization task
    - Results task


    """
    def __init__(self) -> None:
        """

        """
        pass

    def create(self, task_type: str):
        """
        Função para fazer a criação de cara tarefa

        @param task_type: tipo da tarefa de acordo com cada módulo do framework
        @return: instance of task
        """
        task = task_map[task_type]
        task_module = task['module']
        task_class_name = task['class_name']

        module = importlib.import_module(task_module)
        class_ = getattr(module, task_class_name)
        class_object = class_(sys.argv)

        return class_object

