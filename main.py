import subprocess

from src.data.loader import Loader
from external.deploy import TaskExecutor, Xperimentor
from src.parser import json2yaml
import sys
from src.experiments.experiment_handler import ExperimentHandler
from src.experiments.experiment_tasks import ExperimentTask
from external.deploy import Xperimentor, TaskExecutor

if __name__ == "__main__":
    loader = Loader()

    task_executor = TaskExecutor()

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


    print("experiment task")
    print(experiment_tasks)
    dataset_task_command = list(filter(
        lambda x: x['task_name'] == 'dataset_task',
        experiment_tasks
    ))[0]['command']

    preprocessing_task_command = list(filter(
        lambda x: x['task_name'] == 'preprocessing_task',
        experiment_tasks
    ))[0]['command']
    recommenders_task_command = list(filter(
        lambda x: x['task_name'] == 'recommenders_task',
        experiment_tasks
    ))[0]['command']
    metrics_task_command = list(filter(
        lambda x: x['task_name'] == 'metrics_task',
        experiment_tasks
    ))[0]['command']
    metafeatures_task_command = list(filter(
        lambda x: x['task_name'] == 'metafeatures_task',
        experiment_tasks
    ))[0]['command']
    results_task_command = list(filter(
        lambda x: x['task_name'] == 'results_task',
        experiment_tasks
    ))[0]['command']
    visualization_task_command = list(filter(
        lambda x: x['task_name'] == 'visualization_task',
        experiment_tasks
    ))[0]['command']

    output = subprocess.call([dataset_task_command],
                             shell=True)

    print("Output do processo - dataset_task: ", output)

    output = subprocess.call([preprocessing_task_command],
                             shell=True)
    print("Output do processo - preprocessing_task", output)

    #print("recommenders_task_command: ", recommenders_task_command)
    #output = subprocess.call([recommenders_task_command],
     #                        shell=True)
    #print("Output do processo - recommenders_task", output)

