from src.utils import hrf_task_path
from src.tasks.task_factory import TaskFactory
class ExperimentTask:
    def __init__(self):
        # Definição de todas as tarefas do framework (Executadas pelo Task Executor)
        self._task_factory = TaskFactory()


    def generate_command(self, task_type: str) -> str:
        """

        @param task_type:
        @return:
        """
        command = None
        task_obj = task_type
        task_type = task_type['task_name']
        task_path = hrf_task_path()

        if task_type == "dataset_task":
            command = "python " + str(task_path) + "/dataset_task.py"
        if task_type == "metrics_task":
            command = "python " + str(task_path) + "/metrics_task.py"
        if task_type == "metafeatures_task":
            command = "python " + str(task_path) + "/metafeatures_task.py"
        if task_type == "visualization_task":
            command = "python " + str(task_path) + "/visualization_task.py"
        if task_type == "recommenders_task":
            command = "python " + str(task_path) + "/algorithms_task.py"
        if task_type == "preprocessing_task":
            command = "python " + str(task_path) + "/preprocessing_task.py"
        if task_type == "results_task":
            command = "python " + str(task_path) + "/results_task.py"

        task_obj['command'] = command
        return task_obj

    def define_all_tasks_commands(self, tasks: dict) -> dict:
        """

        @param tasks:
        @return:
        """
        archives_tasks = [
            "dataset_task.py",
            "metrics_task.py",
            "metafeatures_task.py",
            "algorithms_task.py",
            "visualization_task.py"
            "preprocessing_task.py",
            "results_task.py"
        ]

        command = None
        tasks_path = hrf_task_path()

        commands = {
            "dataset": ["dataset_task", None],
            "preprocessing": ["preprocessing_task", None],
            "metafeatures": ["metafeatures_task", None],
            "algorithms": ["algorithms_task", None],
            "metrics": ["metrics_task", None],
            "visualization": ["visualization_task", None],
            "results": ["results_task", None]
        }

        for task in archives_tasks:

            for key, value in commands.items():
                which_task = value[0]
                command = self.generate_command(which_task)
                value[1] = command
                continue

        return commands

    def create_task_object(self, task_type: str) -> dict:
        task_name = task_type + "_task"
        return {
            'task': task_type,
            'task_name': task_name,
            'command': None
        }

    def create_tasks_structure(self, default_tasks: list) -> list:
        tasks_structure = []
        for task in default_tasks:
            tasks_structure.append(self.create_task_object(task))
        return tasks_structure


    def define_all_tasks(self) -> dict:
        """
        Cria um dicionário para mapear todas as tarefas

        @return: dict
        """
        tasks = {}
        exp_id = None

        default_tasks = [
            'dataset',
            'preprocessing',
            'metrics',
            'metafeatures',
            'recommenders',
            'visualization',
            'results'
        ]
        tasks_structure = self.create_tasks_structure(default_tasks)
        tasks_structure = list(map(self.generate_command, tasks_structure))
        return tasks_structure