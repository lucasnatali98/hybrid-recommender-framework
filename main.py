import subprocess
from src.data.loader import Loader
from src.parser import json2yaml
import sys
from src.experiments.experiment_handler import ExperimentHandler
from src.experiments.experiment_tasks import ExperimentTask
from external.deploy import Xperimentor, TaskExecutor
from src.utils import beautify_subprocess_output_response, beautify_subprocess_stderr_respose


"""

-> Hibridização -> pesos ()

-> arq

"""

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

    path_to_config_file = "";

    args = sys.argv

    if len(args) == 0:
        path_to_config_file = "config.json"
    else:
        path_to_config_file = args[1]


    all_commands = experiment_task.get_task_commands(experiment_tasks)

    for key, value in all_commands.items():
        output = subprocess.run([value], shell=True, capture_output=True, check=True)
        return_code = output.returncode
        stdout = output.stdout.decode("utf-8")
        stderr = output.stderr.decode("utf-8")
        beautify_output = beautify_subprocess_output_response(return_code)
        beautify_stderr = beautify_subprocess_stderr_respose(stderr)
        print("Output do processo: {}: ".format(key), beautify_output)
        print("Erros: ", beautify_stderr)
