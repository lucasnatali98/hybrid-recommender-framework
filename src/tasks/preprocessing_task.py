import sys
import subprocess
from src.data.loader import Loader
from src.tasks.task import Task
from src.experiments.experiment_handler import ExperimentHandler
from src.utils import hrf_experiment_output_path, process_parameters


class PreProcessingTask(Task):
    def __init__(self, preprocessing, args=None):
        self.experiment_output_dir = hrf_experiment_output_path()

        self.path_to_dataset = self.experiment_output_dir.joinpath("datasets/new_ratings_dataset.csv")
        self.path_to_content_based_dataset = self.experiment_output_dir.joinpath("datasets/items.csv")
        self.path_to_preprocessing_output = self.experiment_output_dir.joinpath("preprocessing/")
        self.loader = Loader()

        self.preprocessing = preprocessing

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

        self.dataset_cf = self.loader.load_csv_file(self.path_to_dataset)
        self.dataset_cb = self.loader.load_csv_file(self.path_to_content_based_dataset)

        self._handle_pre_processing_tasks(self.dataset_cf, self.preprocessing)

    def _handle_pre_processing_tasks(self, dataset, preprocessing):
        """

        @param dataset:
        @param preprocessing:
        @return:
        """
        execution_steps = {}
        items = preprocessing.items[0]  # [[]]
        result = dataset

        for item in items:
            class_name = item.__class__.__name__
            if class_name == "TextProcessing":
                db = self.dataset_cb
                temp_cb = item.pre_processing(db)
                execution_steps[class_name] = temp_cb
                temp_cb.to_csv(
                    self.path_to_preprocessing_output.joinpath("content-based-dataset.csv"),
                    index=False)
                continue

            temp = item.pre_processing(result)
            result = temp
            execution_steps[class_name] = result

        result.to_csv(self.path_to_preprocessing_output.joinpath("preprocessed_dataset.csv"), index=False)

        print("=> Todas as tarefas de pré-processamento foram realizadas e salvas em diretórios temporários\n")


def run_preprocessing_task():
    loader = Loader()
    config_obj = loader.load_json_file("config.json")
    experiments = config_obj['experiments']
    exp_handler = ExperimentHandler(
        experiments=experiments
    )

    experiment = exp_handler.get_experiment("exp1")
    experiment_instances = experiment.instances
    preprocessing_instance = experiment_instances['preprocessing']

    preprocessing_task = PreProcessingTask(preprocessing_instance)
    print("\n")
    print(" => Inicio da tarefa de preprocessamento...")
    preprocessing_task.run()

    # save the preprocessing result

    print(" => Finalização da tarefa de preprocessamento...")


run_preprocessing_task()
