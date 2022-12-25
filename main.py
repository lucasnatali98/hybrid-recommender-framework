import subprocess

from src.data.loader import Loader
from external.deploy import TaskExecutor, Xperimentor
from src.parser import json2yaml
import sys
from src.experiments.experiment_handler import ExperimentHandler
from src.experiments.experiment_tasks import ExperimentTask
from external.deploy import Xperimentor

if __name__ == "__main__":
        loader = Loader()
        config_obj = loader.load_json_file("config.json")

        experiments = config_obj['experiments']

        cluster_info = config_obj['cluster_info']

        recipes_default = config_obj['recipesDefault']

        experiment_dependencies = config_obj['experiment_dependencies']

        experiment_handler = ExperimentHandler(
            experiments=experiments
        )
        experiment_task = ExperimentTask()
        experiment_tasks = experiment_task.define_all_tasks()
        print("Todas as tarefas do experimento")
        print(experiment_tasks)

        xperimentor = Xperimentor()
        xperimentor_config_obj = xperimentor.convert_to_xperimentor_pattern(
            experiments=experiments,
            experiment_dependencies=experiment_dependencies,
            recipes_default=recipes_default,
            cluster_info=cluster_info,
            tasks=experiment_tasks
        )

        with open("experiment_output/configuration_files/xperimentor_yaml_file.yaml", 'w') as file:
            xperimentor_yaml_file = json2yaml(xperimentor_config_obj, file)


       # experiment_results = experiment_handler.run_experiments()

        path_to_config_file = "";

        args = sys.argv

        if len(args) == 0:
            path_to_config_file = "config.json"
        else:
            path_to_config_file = args[1]


       # dataset_task = run_dataset_task()
        print("Dataset task result")
        dataset_task_command = experiment_tasks[0]['command']
        print("dataset task command: ", dataset_task_command)
        command_path = dataset_task_command.split(" ")[1]
        print(command_path)
        output = subprocess.call([dataset_task_command],
                                shell=True)
        print("Output do processo: ", output)
