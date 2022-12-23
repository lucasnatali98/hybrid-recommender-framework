from src.data.loader import Loader
from external.deploy import TaskExecutor, Xperimentor
from src.parser import json2yaml
import json
import sys
from src.data.data_handler import DataHandler
from src.experiments.experiment_handler import ExperimentHandler
from src.data.folds import Folds
from src.tasks.dataset_task import run_dataset_task
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

    xperimentor = Xperimentor()
    xperimentor_config_obj = xperimentor.convert_to_xperimentor_pattern(
        experiments=experiments,
        experiment_dependencies=experiment_dependencies,
        recipes_default=recipes_default,
        cluster_info=cluster_info
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


