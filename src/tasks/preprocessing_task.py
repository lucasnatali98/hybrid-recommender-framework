import sys
import subprocess
from src.data.loader import Loader
from src.tasks.task import Task
from src.experiments.experiment_handler import ExperimentHandler
from src.utils import hrf_experiment_output_path


class PreProcessingTask(Task):
    def __init__(self, preprocessing, args = None):
        self.experiment_output_path = hrf_experiment_output_path()
        self.path_to_dataset = self.experiment_output_path.joinpath("datasets/new_dataset.csv")
        self.loader = Loader()
        self.dataset = self.loader.load_csv_file(self.path_to_dataset)
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

        self._handle_pre_processing_tasks(self.dataset, self.preprocessing)

    def _handle_pre_processing_tasks(self, dataset, preprocessing):
        """

        @param dataset:
        @param preprocessing:
        @return:
        """
        execution_steps = {}
        items = preprocessing.items[0]
        print("Preprocessing items: ")
        print(items)
        for item in items:
            class_name = item.__class__.__name__
            result = item.pre_processing(dataset)
            execution_steps[class_name] = result

        print("Execution Steps: ", execution_steps)
        self._save_splited_dataset(execution_steps['SplitProcessing'])
        print("=> Todas as tarefas de pré-processamento foram realizadas e salvas em diretórios temporários\n")

    def _save_splited_dataset(self, split_processing: dict):
        """

        @param split_processing:
        @return:
        """
        loader = Loader()
        preprocessing_experiment_output_path = hrf_experiment_output_path().joinpath("preprocessing/")
        print("Preprocessing experiment output path: ", preprocessing_experiment_output_path)
        for key, value in split_processing.items():
            if key == 'x_train':
                loader.convert_to("csv", value, preprocessing_experiment_output_path.joinpath("xtrain.csv"))
            if key == 'x_test':
                loader.convert_to("csv", value, preprocessing_experiment_output_path.joinpath("xtest.csv"))
            if key == 'y_train':
                loader.convert_to("csv", value, preprocessing_experiment_output_path.joinpath("ytrain.csv"))
            if key == 'y_test':
                loader.convert_to("csv", value, preprocessing_experiment_output_path.joinpath('ytest.csv'))


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
    print("Preprocessing instance: ")
    print(preprocessing_instance)

    preprocessing_task = PreProcessingTask(preprocessing_instance)

    print(" => Inicio da tarefa de preprocessamento...")
    preprocessing_task.run()

    # save the preprocessing result

    print(" => Finalização da tarefa de preprocessamento...")


run_preprocessing_task()
