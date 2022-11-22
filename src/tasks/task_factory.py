import inspect
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
    "algorithms": {
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
    }
}


class TaskFactory:
    def __init__(self) -> None:
        pass

    def create(self, task_type: str):
        task = task_map[task_type]
        task_module = task['module']
        task_class_name = task['class_name']

        module = importlib.import_module(task_module)
        class_ = getattr(module, task_class_name)
        class_object = class_(sys.argv)

        return class_object

